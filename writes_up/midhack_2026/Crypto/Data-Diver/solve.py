ct="OCHERH{lu_nhnrumi_1968_jt_fv_wuvwv_ixt_cxm}"
key="andrefauve"
def dec(ct,key):
    out=[];ki=0
    for ch in ct:
        if ch.isalpha():
            k=ord(key[ki%len(key)])-97
            base=ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch)-base-k)%26+base));ki+=1
        else:
            out.append(ch)
    return "".join(out)
print("decrypt:",dec(ct,key))
# reverse check: encrypt la_minerve...
def enc(pt,key):
    out=[];ki=0
    for ch in pt:
        if ch.isalpha():
            k=ord(key[ki%len(key)])-97
            base=ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch)-base+k)%26+base));ki+=1
        else:out.append(ch)
    return "".join(out)
print("enc minerve:",enc("OPENNC{la_minerve_1968_et_la_suite_est_ici}",key))
print("enc sdnerve:",enc("OPENNC{la_sdnerve_1968_et_la_suite_est_ici}",key))
