import json, time, urllib.request, urllib.error
from solver import solve

U = "http://challs.hackagou.nc:48983"

def req(path, method='GET', data=None, token=None):
    headers = {}
    if token: headers['X-Run-Token'] = token
    body = None
    if data is not None:
        headers['Content-Type'] = 'application/json'
        body = json.dumps(data).encode()
    r = urllib.request.Request(U+path, data=body, method=method, headers=headers)
    try:
        resp = urllib.request.urlopen(r, timeout=30)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

t0 = time.time()
status, data = req('/api/start', 'POST', {})
run_id = data.get('run_id')
print(f"start: HTTP {status} run_id={run_id} level={data.get('level')} time_left={data.get('time_left')}")
field = data
for i in range(1, 60):
    lvl = field.get('level')
    sol = solve(field)
    if sol is None:
        print(f"[L{lvl}] AUCUNE SOLUTION TROUVEE");
        open('fail_field.json','w').write(json.dumps(field)); break
    st, resp = req('/api/submit_path', 'POST', {'moves': sol, 'nonce': field.get('nonce')}, token=run_id)
    s = resp.get('status')
    if s == 'won' or 'flag' in resp:
        print(f"[L{lvl}] WON apres {len(sol)} coups !  t={time.time()-t0:.1f}s")
        print("FLAG:", resp.get('flag'))
        print("ARCHIVE:", (resp.get('archive') or '')[:400])
        open('won.json','w').write(json.dumps(resp, ensure_ascii=False, indent=1))
        break
    if s == 'lost':
        print(f"[L{lvl}] LOST ({len(sol)} coups): {resp.get('reason')}")
        open('lost_field.json','w').write(json.dumps(field))
        break
    print(f"[L{lvl}] OK ({len(sol)} coups) -> next L{resp.get('level')} phase={resp.get('phase')} time_left={resp.get('time_left')}")
    field = resp
else:
    print("boucle terminee sans victoire")
print(f"total {time.time()-t0:.1f}s")
