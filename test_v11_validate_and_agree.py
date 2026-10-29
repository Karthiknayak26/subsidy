"""TEST FIXTURES ONLY. All data below is obviously synthetic (SYNTH_* ids).
Nothing here is a human or AI rating of benchmark scenarios, and no statistic
computed here may be reported as empirical agreement."""
import tempfile, unittest
from pathlib import Path
import pandas as pd
import v11_validate_and_agree as v

PAIRS = [(f"SYNTH_S{i}", s) for i in range(1, 6) for s in ("SCH_A", "SCH_B")]

def tmpl(rater):
    return pd.DataFrame({"scenario_id": [p[0] for p in PAIRS], "scheme_id": [p[1] for p in PAIRS],
        "scheme_name": "TEST FIXTURE scheme", "rater_id": rater,
        "relevance_score": None, "relevance_rationale": None, "complementarity_notes": None})

def filled(rater, scores):
    d = tmpl(rater)
    d["relevance_score"] = scores
    d["relevance_rationale"] = "TEST FIXTURE rationale"
    return d

S = [0, 1, 2, 3, 0, 1, 2, 3, 1, 2]
EXP = set(PAIRS)

class Tests(unittest.TestCase):
    def test_blank_template_valid(self):
        self.assertTrue(v.validate_template(tmpl("E1"), "E1").ok)

    def test_template_with_prefilled_score_rejected(self):
        d = tmpl("E1"); d.loc[0, "relevance_score"] = 2
        self.assertFalse(v.validate_template(d, "E1").ok)

    def test_wrong_rater_id_rejected(self):
        self.assertFalse(v.validate_template(tmpl("E2"), "E1").ok)

    def test_perfect_agreement(self):
        r = v.agreement_report(filled("E1", S), filled("E2", S))
        self.assertAlmostEqual(r["quadratic_weighted_kappa"], 1.0)
        self.assertAlmostEqual(r["krippendorff_alpha_ordinal"], 1.0)
        self.assertEqual(r["n_mandatory_adjudication"], 0)
        self.assertTrue(r["kappa_meets_threshold"] and r["alpha_meets_threshold"])

    def test_disagreements_identified(self):
        s2 = list(S); s2[0] = 2; s2[3] = 0; s2[4] = 1   # deltas 2, 3, 1
        r = v.agreement_report(filled("E1", S), filled("E2", s2))
        self.assertEqual(r["n_mandatory_adjudication"], 2)
        self.assertEqual(r["n_adjacent_disagreements"], 1)
        self.assertEqual({e["abs_delta"] for e in r["escalation_pairs"]}, {2, 3})

    def test_kappa_hand_computed(self):
        # 2 items: (0,0),(3,3) plus (0,1): known small case, checked against formula by hand
        a = pd.Series([0, 3, 0]).to_numpy(); b = pd.Series([0, 3, 1]).to_numpy()
        k, _ = v.quadratic_weighted_kappa(a, b)
        # O: (0,0)=1,(3,3)=1,(0,1)=1 ; row marg [2,0,0,1], col marg [1,1,0,1]
        import numpy as np
        E = np.outer([2, 0, 0, 1], [1, 1, 0, 1]) / 3
        W = (np.arange(4)[:, None] - np.arange(4)[None, :]) ** 2 / 9
        O = np.zeros((4, 4)); O[0, 0] = O[3, 3] = O[0, 1] = 1
        self.assertAlmostEqual(k, 1 - (W * O).sum() / (W * E).sum())

    def test_constant_ratings_undefined_not_fabricated(self):
        r = v.agreement_report(filled("E1", [2] * 10), filled("E2", [2] * 10))
        self.assertIsNone(r["quadratic_weighted_kappa"])
        self.assertIsNone(r["krippendorff_alpha_ordinal"])
        self.assertIn("undefined", r["kappa_status"])

    def test_missing_and_invalid_scores_flagged_and_excluded(self):
        bad = list(S); bad[0] = None; bad[1] = 7; bad[2] = 1.5; bad[3] = "x"
        d = filled("E1", bad)
        rep = v.validate_submission(d, "E1", EXP)
        self.assertFalse(rep.ok)
        self.assertGreaterEqual(len(rep.errors), 4)
        r = v.agreement_report(d, filled("E2", S))
        self.assertEqual(r["n_pairs_excluded_missing_or_invalid"], 4)
        self.assertEqual(r["n_pairs_rated_by_both"], 6)

    def test_missing_rationale_rejected(self):
        d = filled("E1", S); d.loc[0, "relevance_rationale"] = ""
        self.assertFalse(v.validate_submission(d, "E1", EXP).ok)

    def test_missing_duplicate_and_extra_pairs_rejected(self):
        d = filled("E1", S).iloc[:-1]
        self.assertFalse(v.validate_submission(d, "E1", EXP).ok)
        d = pd.concat([filled("E1", S), filled("E1", S).iloc[[0]]], ignore_index=True)
        self.assertFalse(v.validate_submission(d, "E1", EXP).ok)
        d = filled("E1", S); d.loc[0, "scenario_id"] = "SYNTH_S99"
        self.assertFalse(v.validate_submission(d, "E1", EXP).ok)

    def test_mismatched_e1_e2_pairs_rejected(self):
        e2 = filled("E2", S); e2.loc[0, "scheme_id"] = "SCH_Z"
        self.assertFalse(v.validate_pair_match(filled("E1", S), e2).ok)

    def test_column_rename_rejected(self):
        d = filled("E1", S).rename(columns={"relevance_score": "score"})
        self.assertFalse(v.validate_submission(d, "E1", EXP).ok)

    def test_section_b_numeric_scores_rejected(self):
        ok = pd.DataFrame({"scenario_id": ["SYNTH_S1"], "scheme_id": ["SCH_B1"], "qualitative_notes": ["TEST FIXTURE"]})
        self.assertTrue(v.validate_section_b(ok).ok)
        bad = ok.assign(relevance_score=[2])
        self.assertFalse(v.validate_section_b(bad).ok)
        bad2 = ok.assign(score=[1])
        self.assertFalse(v.validate_section_b(bad2).ok)

    def test_consensus_never_alters_raw_and_refuses_raw_dir(self):
        e1, e2 = filled("E1", S), filled("E2", [3] + S[1:])
        e1c, e2c = e1.copy(), e2.copy()
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "consensus" / "ledger.csv"
            led = v.write_consensus_ledger(e1, e2, out)
            self.assertTrue(out.exists())
            with self.assertRaises(ValueError):
                v.write_consensus_ledger(e1, e2, Path(t) / "raw" / "ledger.csv")
        pd.testing.assert_frame_equal(e1, e1c); pd.testing.assert_frame_equal(e2, e2c)
        self.assertEqual(led.loc[0, "status"], "PENDING_ADJUDICATION_PANEL")
        self.assertTrue(pd.isna(led.loc[0, "consensus_score"]))
        # reliability on raw ratings is unchanged by writing a ledger
        self.assertEqual(v.agreement_report(e1, e2), v.agreement_report(e1c, e2c))

    def test_context_missing_fails_closed(self):
        packet = tmpl("E1")
        sc = pd.DataFrame({"scenario_id": ["SYNTH_S1"]})
        sh = pd.DataFrame({"scheme_id": ["SCH_A"], "scheme_name": ["x"]})
        self.assertFalse(v.validate_context(sc, sh, packet).ok)

    def test_context_complete_passes_and_blank_field_fails(self):
        packet = tmpl("E1")
        sc = pd.DataFrame([{c: "TEST FIXTURE" for c in v.SCENARIO_REQUIRED}] * 1)
        sc = pd.concat([sc.assign(scenario_id=f"SYNTH_S{i}") for i in range(1, 6)], ignore_index=True)
        sh = pd.DataFrame([{c: "TEST FIXTURE" for c in v.SCHEME_REQUIRED}] * 1)
        sh = pd.concat([sh.assign(scheme_id=s) for s in ("SCH_A", "SCH_B")], ignore_index=True)
        self.assertTrue(v.validate_context(sc, sh, packet).ok)
        sc.loc[0, "primary_acute_crisis"] = ""
        self.assertFalse(v.validate_context(sc, sh, packet).ok)

    def test_context_with_leaked_label_column_rejected(self):
        packet = tmpl("E1")
        sc = pd.DataFrame([{c: "T" for c in v.SCENARIO_REQUIRED}]).assign(scenario_id="SYNTH_S1", heuristic_rank=1)
        sh = pd.DataFrame([{c: "T" for c in v.SCHEME_REQUIRED}]).assign(scheme_id="SCH_A")
        self.assertFalse(v.validate_context(sc, sh, packet).ok)

    def test_context_missing_scenario_row_rejected(self):
        packet = tmpl("E1")
        sc = pd.DataFrame([{c: "T" for c in v.SCENARIO_REQUIRED}]).assign(scenario_id="SYNTH_S1")
        sh = pd.concat([pd.DataFrame([{c: "T" for c in v.SCHEME_REQUIRED}]).assign(scheme_id=s) for s in ("SCH_A", "SCH_B")])
        self.assertFalse(v.validate_context(sc, sh, packet).ok)

if __name__ == "__main__":
    unittest.main(verbosity=2)
