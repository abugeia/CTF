# Extrait l'archive ZIP concaténée après le chunk IEND de A330neo2bis.png
import io, zipfile
d = open('A330neo2bis.png','rb').read()
z = zipfile.ZipFile(io.BytesIO(d[d.index(b'IEND')+8:]))
for i in z.infolist():
    print(i.filename, 'chiffré' if i.flag_bits & 1 else 'clair', i.comment)
    print(z.read(i).decode())
print('commentaire zip:', z.comment)
