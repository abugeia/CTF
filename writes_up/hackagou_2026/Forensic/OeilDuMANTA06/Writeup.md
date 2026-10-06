# L'Œil du MANTA-06 (HacKagou 2026) — Forensic

**Flag :** `OPENNC{...}` *(flag dynamique par instance — non capturé ici)*
**Valeur :** 100 pts · **Auteur :** Ketsui
**Statut :** 🟢 **résolu par l'équipe** (`solved_by_me: true`) ; ce writeup reste un **plan
de méthode** (session sans instance). Instances désormais injouables (infra `ctfd-whale`
démontée post-event : `POST container` → *Container creation failed*).

## Énoncé

> Le MANTA-06 a établi une liaison avec une ancienne caméra de surveillance **ARGOS-03**, dont l'interface est **verrouillée**. « Le **dernier paquet réseau** transmis par le MANTA-06 pourrait permettre de découvrir ce qu'elle protège. N'hésitez pas à explorer la caméra. »
> *Hors sujet : un jeuuu d'acteur digne de wish.* ← indice (acteur « bas de gamme » → piste pour un mot de passe/référence).

## Reconnaissance / analyse

Forensic réseau + exploration d'interface de caméra :
- **« dernier paquet réseau »** → un **pcap** (ou une capture fournie par l'instance) contenant vraisemblablement des **identifiants** (HTTP Basic, formulaire, RTSP, Telnet) de la caméra ARGOS-03.
- La blague « jeu d'acteur digne de wish » est un **indice déguisé** : nom d'acteur de seconde zone → peut être un **mot de passe**, un **nom d'utilisateur**, ou une référence à chercher (les caméras IP ont souvent des creds par défaut).

## Plan de résolution

1. Démarrer l'instance, récupérer le **paquet / la capture** proposé par la caméra ou le MANTA-06.
2. Analyser (`wireshark` / `tshark` / `strings`) : extraire credentials, URL, token, flux.
   ```bash
   tshark -r capture.pcap -Y 'http || telnet || rtsp' -V
   strings capture.pcap | grep -iE 'user|pass|auth|login|OPENNC'
   ```
3. Se connecter à l'interface ARGOS-03 avec les creds trouvés (ou l'indice « acteur »).
4. Explorer la caméra (flux, fichiers, config) → trouver ce qu'elle protège → `OPENNC{...}`.

## Flag

```
OPENNC{...}
```
