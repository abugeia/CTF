# Le télégraphe abyssal (HacKagou 2026) — Web

**Flag :** `OPENNC{...}` *(flag dynamique par instance — non capturé ici)*
**Valeur :** 100 pts · **Auteur :** Yoan
**Statut :** 🟢 **résolu par l'équipe** (`solved_by_me: true`) ; ce writeup reste un **plan
de méthode** (session sans instance). Instances désormais injouables (infra `ctfd-whale`
démontée post-event : `POST container` → *Container creation failed*).

## Énoncé

> Une vieille balise mécanique émet encore (récif de Baker). « Le canal est désynchronisé et l'accès à la console reste verrouillé : un **régulateur d'ondes filtre les fréquences**, un **contrôle d'identité maintient chaque visiteur au rang GUEST**. Les Ferrailleurs accordaient un **code Morse précis**, puis présentaient une **signature de relais** particulière pour s'élever au rang **ADMIN**. » Mission : accorder la console, franchir le filtre d'identité et récupérer le **premier fragment du journal de Varn**.

## Reconnaissance / analyse

Trois verrous distincts, dans l'ordre :
1. **Accorder la résonance** : un paramètre de « fréquence » à régler sur la bonne valeur (probablement un champ/param de requête, ou une valeur à deviner — le **code Morse** décode sûrement cette fréquence).
2. **Code Morse** : une séquence affichée (ou audio) à décoder → donne un mot/une fréquence.
3. **Privesc GUEST → ADMIN** via une « signature de relais » : typiquement un **cookie de rôle**, un **JWT** (`role: guest`→`admin`, `alg:none`), un header, ou un paramètre caché.

## Plan de résolution

1. Démarrer l'instance, ouvrir `http://challs.hackagou.nc:{port}`.
2. Inspecter la page (source, JS, requêtes réseau, cookies, `/robots.txt`, routes).
3. Décoder le **Morse** affiché (dcode / à la main) → obtenir la valeur de « résonance/fréquence » attendue, la soumettre.
4. Analyser le mécanisme d'identité :
   - cookie en clair / base64 (`role=guest`) → forger `role=admin` ;
   - JWT → tester `alg:none`, clé faible (`jwt_tool`, bruteforce HS256) ;
   - champ caché / paramètre `is_admin`.
5. Une fois ADMIN + canal accordé, lire la transmission réservée → **fragment du journal** → `OPENNC{...}`.

## Flag

```
OPENNC{...}
```
