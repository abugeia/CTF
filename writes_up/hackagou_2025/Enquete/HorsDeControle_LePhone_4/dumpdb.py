import sqlite3,sys,os
for root,_,fs in os.walk('Dump'):
  for f in fs:
    p=os.path.join(root,f)
    try:
      with open(p,'rb') as h:
        if h.read(16)!=b'SQLite format 3\x00': continue
      c=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
      for (t,) in c.execute("select name from sqlite_master where type='table'"):
        try:
          rows=c.execute(f'select * from "{t}"').fetchall()
        except Exception as e: continue
        for r in rows: print(p,t,r)
    except Exception as e: print('ERR',p,e,file=sys.stderr)
