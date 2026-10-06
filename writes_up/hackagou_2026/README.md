# HacKagou 2026 — Write-ups

Édition 2026 (univers **Abysséa / LÉVIATHAN / NÉRÉIDE**, équipage KAGOU-06).
Plateforme https://ctf.hackagou.nc — équipe **nggyu** (mode équipes).

> **État au 2026-10-06 (post-event).** Le CTF s'est terminé le 1er octobre. L'équipe a
> validé **18 / 27** challenges. L'**infra conteneurs `ctfd-whale` est démontée** :
> `POST …/container` renvoie *Container creation failed* → les challenges à instance
> (`dynamic_docker[_team]`) sont **injouables à distance** désormais (la soumission de flag
> reste ouverte). Les challenges **IoT** et une partie des Physique/Crypto comportent du
> matériel **sur site** (NFC, BLE, gravure laser, diffusion en salle). Modèle :
> [_TEMPLATE.md](_TEMPLATE.md).

Légende : ✅ résolu (flag validé) · 🟢 résolu par l'équipe (writeup = plan ; flag dynamique
par instance non recopié) · 🟠 partiel / matériel récupéré · 🔴 non résolu (vecteur
introuvable, infra morte ou présence physique) · 🔒 prérequis manquant.

| Catégorie | Challenge | Pts | Statut | Write-up |
|---|---|---|---|---|
| Ephémère | L'héritage du commandant | 10 | ✅ `Capitaine Nepo` (QCM, piège népotisme) | [Ephemere/HeritageDuCommandant/Writeup.md](Ephemere/HeritageDuCommandant/Writeup.md) |
| Crypto | La piste atlante | 50 | 🟢 résolu équipe (alphabet Atlante) | [Crypto/LaPisteAtlante/Writeup.md](Crypto/LaPisteAtlante/Writeup.md) |
| Crypto | La chaufferie piégée | 250 | 🔴 non résolu (vecteur « 5409th position » introuvable) | [Crypto/LaChaufferiePiegee/Writeup.md](Crypto/LaChaufferiePiegee/Writeup.md) |
| Crypto | Télégraphe Abyssal [1/2] : Dans tous les sens | 250 | 🟠 matériel récupéré (totem Morse = ALPHABET) · instance down | [Crypto/TelegrapheAbyssal_1/Writeup.md](Crypto/TelegrapheAbyssal_1/Writeup.md) |
| IA | L'echo de NÉRÉIDE | 100 | ✅ (fuite du system prompt) | [IA/EchoDeNereide/Writeup.md](IA/EchoDeNereide/Writeup.md) |
| IA | Le filtre abyssal | 487 | ✅ (contournement filtre de sortie) | [IA/LeFiltreAbyssal/Writeup.md](IA/LeFiltreAbyssal/Writeup.md) |
| IA | Les cartes perforées de Varn | 246 | ✅ (prompt injection via PDF `/analyze`) | [IA/CartesPerforeesDeVarn/Writeup.md](IA/CartesPerforeesDeVarn/Writeup.md) |
| Web | Escape | 100 | ✅ | [Web/Escape/Writeup.md](Web/Escape/Writeup.md) |
| Web | La salle des cartes | 100 | ✅ | [Web/LaSalleDesCartes/Writeup.md](Web/LaSalleDesCartes/Writeup.md) |
| Web | La chaufferie de laiton | 100 | ✅ | [Web/LaChaufferieDeLaiton/Writeup.md](Web/LaChaufferieDeLaiton/Writeup.md) |
| Web | Le télégraphe abyssal | 100 | 🟢 résolu équipe (Morse + privesc GUEST→ADMIN) | [Web/TelegrapheAbyssal/Writeup.md](Web/TelegrapheAbyssal/Writeup.md) |
| Web | La Passe Sans Retour | 250 | ✅ | [Web/LaPasseSansRetour/Writeup.md](Web/LaPasseSansRetour/Writeup.md) |
| Web | La passerelle LÉVIATHAN | 249 | ✅ (XFF `127.0.0.1` + WAF casse `commander` + 3 clés) | [Web/LaPasserelleLeviathan/Writeup.md](Web/LaPasserelleLeviathan/Writeup.md) |
| Pwn | Le régulateur de pression | 100 | ✅ (exploit vérifié via `nc`) | [Pwn/LeRegulateurDePression/Writeup.md](Pwn/LeRegulateurDePression/Writeup.md) |
| Pwn | Le cœur de laiton | 245 | ✅ | [Pwn/LeCoeurDeLaiton/Writeup.md](Pwn/LeCoeurDeLaiton/Writeup.md) |
| Forensic | La backdoor secrète | 100 | ✅ `OPENNC{L3v14th4n_v41ncr4}` (PowerShell fileless) | [Forensic/LaBackdoorSecrete/Writeup.md](Forensic/LaBackdoorSecrete/Writeup.md) |
| Forensic | Le beacon fatal | 94 | ✅ | [Forensic/LeBeaconFatal/Writeup.md](Forensic/LeBeaconFatal/Writeup.md) |
| Forensic | L'Œil du MANTA-06 | 100 | 🟢 résolu équipe (pcap caméra ARGOS-03) | [Forensic/OeilDuMANTA06/Writeup.md](Forensic/OeilDuMANTA06/Writeup.md) |
| Stégano | Echo du Legacy | 250 | ✅ (flag par membre d'équipe) | [Stegano/EchoDuLegacy/Writeup.md](Stegano/EchoDuLegacy/Writeup.md) |
| OSINT | Le tunnel secret vers Abysséa | 249 | ✅ `OPENNC{Apogoti}` | [OSINT/TunnelSecretAbyssea/Writeup.md](OSINT/TunnelSecretAbyssea/Writeup.md) |
| OSINT | Origine du Léviathan | 100 | 🔴 injouable (infra conteneurs down) | [OSINT/OrigineDuLeviathan/Writeup.md](OSINT/OrigineDuLeviathan/Writeup.md) |
| OSINT | Le Dernier Vol du MANTA-06 | 250 | 🔴 injouable (infra conteneurs down) | [OSINT/DernierVolDuMANTA06/Writeup.md](OSINT/DernierVolDuMANTA06/Writeup.md) |
| Physique | Le sceau du graveur | 222 | ✅ (ordre VARN-041 libéré à distance, flag récupéré) | [Physique/LeSceauDuGraveur/Writeup.md](Physique/LeSceauDuGraveur/Writeup.md) |
| IoT | Le Signal de l'Aïeul | 340 | 🔴 sur site (balise BLE Eddystone) | [IoT/SignalDeLAieul/Writeup.md](IoT/SignalDeLAieul/Writeup.md) |
| IoT | La Ronde des Automates | 200 | 🔴 sur site (3 tags NFC) | [IoT/RondeDesAutomates/Writeup.md](IoT/RondeDesAutomates/Writeup.md) |
| IoT | L'Obole de LÉVIATHAN | 400 | 🔴 sur site (paiement NFC/EMV) | [IoT/LOboleDeLeviathan/Writeup.md](IoT/LOboleDeLeviathan/Writeup.md) |
| Easter Egg | Taylor's Version | 250 | 🟠 transverse (rien hors instance) | [EasterEgg/TaylorsVersion/Writeup.md](EasterEgg/TaylorsVersion/Writeup.md) |

**Divers — Le HacKagou édition 2026 (OBLIGATOIRE, 0 pt)** : validé (QCM d'accueil, pas de flag OPENNC).

## Restant (instances relancées le 2026-10-06)

- **Web #40 La passerelle LÉVIATHAN** : ✅ résolu — voir le write-up (bypass IP + WAF + 3 clés reconstituées depuis les actes 1-3).
- **OSINT #20 Le Dernier Vol du MANTA-06** : instance relancée, en cours d'analyse.
- **OSINT #28 Origine du Léviathan** : géoloc des 6 photos — nécessite l'instance.
- **Crypto #31 Télégraphe** : télégramme (instance) à lire « dans tous les sens » avec la clé **ALPHABET** (totem Morse récupéré).
- **Crypto #45 Chaufferie piégée** : seul challenge 100 % hors-instance encore ouvert — tous les vecteurs stégo/LSB/C2PA/constantes ont été éliminés, l'indice « 5409th position » reste à percer.

> Note : la création d'instance **via l'API token échoue** (`Container creation failed`) ;
> les instances doivent être démarrées **depuis le navigateur** (session CTFd de l'équipe).

## Fichiers / infra

Fichiers des challenges téléchargés dans `ctfd-downloads/` (gitignoré) puis copiés dans le
dossier du challenge si utiles. **API CTFd** : token dans `.envrc` (`CTFD_TOKEN`), headers
`Authorization: Token …` **+ `Accept` + `Content-Type: application/json`** (sans
`Content-Type` → 302 `/login`). Le MCP `ctfd` étant instable (déconnexions), passer par
`curl`/Python sur l'API REST est le fallback fiable.
