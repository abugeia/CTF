import json
from collections import deque

COMMANDS = ['N','S','W','E','.']
VECTORS  = {'N':(0,-1),'S':(0,1),'W':(-1,0),'E':(1,0),'.':(0,0)}
CURRENTS = {'^':(0,-1),'v':(0,1),'<':(-1,0),'>':(1,0)}

def build(field):
    n = field['size']; cells = n*n; cycle = field['cycle']
    terrain = ''.join(field['terrain'])
    phase0 = field['phase']
    occupied = [[0]*cells for _ in range(cycle)]
    closed   = [[0]*cells for _ in range(cycle)]
    crossings= [set() for _ in range(cycle)]
    def positions(clock):
        return [((s['x']+s['vx']*clock) % n, s['y']) for s in field['sentries']]
    for clock in range(cycle):
        before = positions(clock); after = positions(clock+1)
        for i in range(len(before)):
            oldc = before[i][1]*n + before[i][0]
            newc = after[i][1]*n + after[i][0]
            occupied[clock][oldc] = 1
            crossings[clock].add(newc*cells + oldc)
        for g in field['shutters']:
            if (clock + g['offset']) % g['period'] not in g['open']:
                closed[clock][g['y']*n + g['x']] = 1
    def safe(x,y,clock):
        if x<0 or y<0 or x>=n or y>=n: return False
        c = y*n+x
        cm = clock % cycle
        return terrain[c] != '#' and not occupied[cm][c] and not closed[cm][c]
    def destination(x,y,clock,cmd):
        phase = clock % cycle
        current = y*n+x
        nextClock = phase+1
        dx,dy = VECTORS[cmd]
        nx,ny = x+dx, y+dy
        if not safe(nx,ny,nextClock): return -1
        cell = ny*n+nx
        if (current*cells + cell) in crossings[phase]: return -1
        drift = CURRENTS.get(terrain[cell])
        if drift:
            nx += drift[0]; ny += drift[1]
            if not safe(nx,ny,nextClock): return -1
            cell = ny*n+nx
        return cell
    relays = [tuple(r) for r in field['relays']]
    exit_ = tuple(field['exit'])
    def advance(state, cmd):
        x,y,t,r = state
        cell = destination(x,y, phase0+t, cmd)
        if cell < 0: return None
        nx, ny = cell % n, cell // n
        nr = r
        if nr < len(relays) and (nx,ny)==relays[nr]:
            nr += 1
        if (nx,ny)==exit_ and nr != len(relays):
            return None  # interlock
        return (nx,ny,t+1,nr)
    start = (field['start'][0], field['start'][1], 0, 0)
    def complete(s):
        return (s[0],s[1])==exit_ and s[3]==len(relays)
    return start, advance, complete, cycle, phase0, field['max_moves']

def solve(field):
    start, advance, complete, cycle, phase0, max_moves = build(field)
    if complete(start): return ''
    seen = {(start[0],start[1],start[3],(phase0+start[2])%cycle)}
    q = deque([(start,'')])
    while q:
        state, path = q.popleft()
        if len(path) >= max_moves: continue
        for cmd in COMMANDS:
            ns = advance(state, cmd)
            if ns is None: continue
            if complete(ns): return path+cmd
            key = (ns[0],ns[1],ns[3],(phase0+ns[2])%cycle)
            if key in seen: continue
            seen.add(key)
            q.append((ns, path+cmd))
    return None

if __name__=='__main__':
    import sys
    f=json.load(open(sys.argv[1]))
    sol=solve(f)
    print('solution:',repr(sol),'len',len(sol) if sol else None)
