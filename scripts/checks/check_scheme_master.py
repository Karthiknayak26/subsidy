import json

with open('scheme_database/processed/scheme_master.json') as f:
    schemes = json.load(f)

print(f'Total schemes: {len(schemes)}')
for s in schemes:
    sid = s['scheme_id']
    name = s['scheme_name']
    url = s.get('official_source_url', '')
    doc = s.get('official_document_url', '')
    audit = s.get('audit_status', '')
    vdate = s.get('verification_date', '')
    print(f'{sid}: {name[:70]} | URL: {url} | audit: {audit} | verified: {vdate}')
    print(f'  Doc: {doc}')
