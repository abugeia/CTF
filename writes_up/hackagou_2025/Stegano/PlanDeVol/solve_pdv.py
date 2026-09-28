# Extrait le caractère caché dans le User-Agent (juste avant "Gecko/") de chaque requête HTTP
import re
from scapy.all import rdpcap, Raw
pk = rdpcap('HK2025_pdv.pcap')
out = ''
hosts=set()
for p in pk:
    if Raw in p:
        d = bytes(p[Raw])
        m = re.search(rb'\)  (.)Gecko/', d)
        if m: out += m.group(1).decode()
        h=re.search(rb'Host: (\S+)',d)
        if h: hosts.add(h.group(1))
print(out); print(hosts)
