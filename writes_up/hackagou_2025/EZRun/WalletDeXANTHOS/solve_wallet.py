# Wallet de XANTHOS : retrouve l'ordre des 4 mots manquants et dérive l'adresse Dogecoin (BIP44 m/44'/3'/0'/0/0)
# uv run --with bip-utils python solve_wallet.py
import itertools
from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip44, Bip44Coins, Bip44Changes

template = "W1 during W3 method snake gadget assault agree W9 mosquito daring W12".split()
slots = [0, 2, 8, 11]
words = ["police", "prison", "satoshi", "gold"]
val = Bip39MnemonicValidator()
for perm in itertools.permutations(words):
    w = template[:]
    for s, x in zip(slots, perm):
        w[s] = x
    m = " ".join(w)
    if not val.IsValid(m):          # checksum BIP39 : ~1 ordre sur 16 passe
        continue
    seed = Bip39SeedGenerator(m).Generate()
    acc = (Bip44.FromSeed(seed, Bip44Coins.DOGECOIN).Purpose().Coin().Account(0)
           .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0))
    addr = acc.PublicKey().ToAddress()
    ok = addr.lower().startswith("dmy") and addr.endswith("aNN")
    print("MATCH" if ok else "     ", addr, "|", m)
