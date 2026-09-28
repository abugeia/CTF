# Extraction des SMS (app com.android.messaging) et de l'historique navigateur (Jelly)
import sqlite3, datetime
B = 'Dump/data-1/com.android.messaging/databases/bugle_db'
H = 'Dump/data-1/org.lineageos.jelly/databases/HistoryDatabase'
ts = lambda ms: datetime.datetime.utcfromtimestamp(ms/1000).isoformat()+'Z'
c = sqlite3.connect(B)
for pid, mid, text, t in c.execute('select _id,message_id,text,timestamp from parts'):
    print(f'[{ts(t)}] part {pid} (msg {mid}): {text!r}')
for r in c.execute('select normalized_destination, full_name from participants'):
    print('participant', r)
h = sqlite3.connect(H)
for _id, t, title, url in h.execute('select * from history'):
    print(f'[{ts(t)}] {title} -> {url[:120]}')
