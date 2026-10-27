import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/paper_claim_audit.json', encoding='utf-8') as f:
    pa = json.load(f)

for i, x in enumerate(pa):
    claim = x.get('claim') or ''
    c_yr = x.get('claimed_year')
    f_yr = x.get('year')
    title = x.get('found') or 'NOT FOUND'
    status = 'MATCH' if (c_yr == f_yr and title != 'NOT FOUND') else 'MISMATCH/NOT FOUND'
    print(f"{i+1}. [{status}] Claimed: '{claim[:45]}' ({c_yr}) -> Found: '{title[:45]}' ({f_yr})")
