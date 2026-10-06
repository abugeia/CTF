# L'Obole de LÉVIATHAN (HacKagou 2026) — IoT

**Flag :** `OPENNC{...}` *(à compléter sur place)*
**Valeur :** 400 pts (dynamique) · **Auteur :** GiGaWaTT
**Statut :** 🔴 **présence physique requise** — lecteur NFC dans la salle, aucun fichier ni instance.

## Énoncé

> Une vieille console de sécurité reliée à un coffre-fort exige un **« Module d'Authentification »**.
> Les badges de service et « puces de cantine » posés sur le capteur sont **rejetés** (« puces passives »)
> ; la machine exige un **« Flux d'émission dynamique sécurisé »**.
> Notes du Capitaine Nepo : *« LÉVIATHAN vérifie l'existence d'un protocole d'échange de surface très
> spécifique, une forme "d'obole" moderne. »*
> Rendez-vous physiquement devant la console LÉVIATHAN dans la salle. Trouvez le bon objet pour
> satisfaire la curiosité du capteur et extraire le flag.

Fichiers : aucun (uniquement l'illustration `2026-Lobole-LEVIATAN.jpeg`). Type CTFd `dynamic`, sans instance.

## Reconnaissance (décodage de l'énoncé)

| Indice | Lecture |
|---|---|
| « capteur », badges, puces de cantine | lecteur **NFC 13,56 MHz** (ISO 14443) |
| « puces passives » rejetées | les tags MIFARE Classic / NTAG (badges, cartes cantine) ne suffisent pas |
| « Flux d'émission dynamique sécurisé » | une carte qui répond par un **cryptogramme dynamique** : **EMV sans contact** (carte bancaire ou paiement mobile tokenisé) |
| « obole » | la pièce donnée à Charon pour la traversée → **paiement** |
| « vérifie l'existence d'un protocole » | le lecteur se contente de **détecter une application de paiement**, il ne débite rien |

Concrètement, le lecteur doit envoyer un `SELECT PPSE` (`2PAY.SYS.DDF01`) et regarder si un AID de
paiement répond (Visa `A0000000031010`, Mastercard `A0000000041010`, CB `A0000000421010`…). Un badge
MIFARE ne parle pas ISO 7816-4/APDU, d'où le rejet.

## Exploitation (à faire sur place)

1. Présenter au capteur une **carte bancaire sans contact**, ou mieux un **smartphone avec Google
   Wallet / Apple Pay** (émulation de carte = « émission dynamique », jeton tokenisé, donc pas de PAN
   réel exposé).
2. Si le lecteur veut un AID précis, émuler la réponse avec une app **HCE** (Android, ex. « NFC Card
   Emulator ») ou un Proxmark3 (`hf 14a sim` + script APDU) qui répond au `SELECT PPSE`.
3. La console affiche alors le flag `OPENNC{...}`.

> ⚠️ Aucun paiement n'est déclenché par un simple `SELECT`, mais préférer un téléphone (jeton) à une
> carte physique (PAN lisible par le lecteur).

## Flag

```
OPENNC{...}
```
