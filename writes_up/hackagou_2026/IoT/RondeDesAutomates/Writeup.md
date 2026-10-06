# La Ronde des Automates (HacKagou 2026) — IoT

**Flag :** `OPENNC{...}` *(à compléter)*
**Valeur :** 200 pts (dynamique) · **Auteur :** GiGaWaTT · **Statut :** 🔴 **présence physique (NFC) requise** — non résoluble à distance.

## Énoncé

> Le Capitaine Nepo a installé **3 plaques de maintenance magnétiques déconnectées** à travers le secteur. Ces relais d'urgence utilisent une **induction à ultra-courte portée**. « En approchant votre terminal de ces **3 sceaux dissimulés dans la salle**, vous pourrez extraire les fragments de données restants. »

> « Inspectez les environs, retrouvez les 3 plaques et assemblez leurs fragments pour reconstituer le code d'accès de la passerelle. »

**Positions des sceaux (données dans l'énoncé)** :
1. sur **un des yeux de la pieuvre** ;
2. sur **la pieuvre ouverte, à la ventouse détachée** ;
3. sur **le porte-chef (chapeau ?) du pirate**.

→ éléments de **décor de la salle** (pieuvres, pirate) : chercher des autocollants/jetons NFC collés dessus.

Illustration : `2026-Ronde-Automate.jpeg`. Type CTFd `dynamic`, aucun fichier, aucune instance.

## Analyse / approche (sur place)

Challenge **NFC / RFID** :
- 3 **tags** (induction ultra-courte portée = NFC 13,56 MHz probable) cachés **dans la salle**, aux 3 positions ci-dessus.
- L'ordre des fragments suit probablement l'ordre de l'énoncé (1er, 2e, dernier sceau).
- Les lire avec un **smartphone NFC** (NFC Tools, TagInfo) ou un **Proxmark/PN532**.
- Chaque tag = 1 **fragment** ; recomposer les 3 fragments → flag.
- Prévoir les formats : NDEF texte/URL, données brutes en secteurs Mifare, éventuellement protégées par clé.

> ⚠️ Nécessite d'être dans la salle avec un lecteur NFC. À traiter sur site.

## Flag

```
OPENNC{...}
```
