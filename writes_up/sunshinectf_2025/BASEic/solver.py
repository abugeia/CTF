import base64

part1_encoded = "c3Vue2MwdjNyMW5nX3V"
part2_encoded = "yX0I0NTM1fQ=="

part1_decoded = base64.b64decode(part1_encoded + "==").decode()
part2_decoded_bytes = base64.b64decode(part2_encoded)

print(f"Partie 1 : {part1_decoded}")
print(f"Partie 2 (hex) : {part2_decoded_bytes.hex()}")

# Je vais essayer de reconstruire le flag manuellement
# sun{c0v3r1ng_up_b4s3s}