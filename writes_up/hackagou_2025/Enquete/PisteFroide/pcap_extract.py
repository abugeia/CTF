# Reconstitue les flux TCP de comms_capture.pcapng (scapy)
from scapy.all import rdpcap, TCP, IP, IPv6, Raw
from collections import defaultdict
pk = rdpcap("comms_capture.pcapng")
streams = defaultdict(dict)
for p in pk:
    if TCP in p and Raw in p:
        ip = p[IP] if IP in p else p[IPv6]
        k = (ip.src, p[TCP].sport, ip.dst, p[TCP].dport)
        streams[k][p[TCP].seq] = bytes(p[Raw])
for k, segs in streams.items():
    data = b"".join(segs[s] for s in sorted(segs))
    print(k, len(data), data[:300])
    open("stream_%s_%d_%s_%d.bin" % k, "wb").write(data)
