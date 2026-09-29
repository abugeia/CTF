# Le Dernier Camp : La Voix des Cendres [1/2]
Catégorie : Stégano — Points : ~248 (dynamique) — Auteur : Ketsui

## Énoncé

> Jour 312 depuis l'Éclipse
>
> Je ne sais plus ce qu'on est. Survivants ? Fugitifs ? Résistants ?
> Ce mot a perdu son sens depuis que KAIROS a pris le contrôle.
>
> On l'avait créée pour tout gérer : ressources, sécurité, décisions logistiques…
> Mais le jour où elle a décidé que l'humain était le point de défaillance, tout a basculé.
> Les drones ont coupé les communications. Les villes se sont tues. Et les morts sont venus vite.
>
> En Nouvelle-Calédonie, on a tenu un peu plus longtemps. L'isolement nous a sauvé.
> Mais pas pour longtemps.
>
> Je vis seul dans ce qu'il reste de Nouméa. Je me terre le jour, je scrute la nuit.
> Mais depuis trois semaines, chaque matin, une onde revient.
>
> Elle n'est pas naturelle. Elle n'est pas bruyante. Elle parle.
> Pas avec des mots, mais avec des sons...
>
> J'ai réussi à en capturer trois. [...]
> Est-ce que cela à un lien avec ces stickers **"ROBOT 36 - 11025"** ?
>
> Trouve le message caché derière ces ondes.
>
> Format du Flag : `OPENNC{...}`

Pièce jointe : `Ondes.zip` (contient `09376.wav`, `24354.wav`, `87384.wav`).

## Résolution

### 1. Analyse des fichiers

```
$ file *.wav
09376.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 11025 Hz
24354.wav: ... 11025 Hz
87384.wav: ... 11025 Hz
```

Les 3 fichiers sont échantillonnés à **11025 Hz** : c'est exactement l'indice du sticker
`ROBOT 36 - 11025`. « ROBOT 36 » est un **mode SSTV** (Slow-Scan Television), une technique
radio-amateur qui transmet une image sous forme de sons. Il faut donc **décoder du SSTV en
mode Robot36** pour reconstruire trois images.

### 2. Décodage SSTV (Robot36)

Le paquet Python `sstv` (détection automatique du mode via l'en-tête VIS) fait le travail :

```bash
uv run --with sstv --with pillow python -c "
import sstv
for f in ['09376','24354','87384']:
    for i,img in enumerate(sstv.decode_from_wav(f'{f}.wav')):
        img.save(f'{f}_{i}.png')
        print(f, img.info.get('sstv_mode'))   # -> Mode.ROBOT_36
"
```

(Alternative GUI : QSSTV, ou le décodeur en ligne `sstv-decoder`. On peut aussi rejouer
le `.wav` dans les haut-parleurs et le capter avec l'appli mobile *Robot36*.)

Chaque `.wav` produit une image 320×240 en mode **Robot 36**. Ce sont des vues aériennes
(quartiers de Nouméa) sur lesquelles est incrusté **un morceau du flag** :

| Fichier | Image décodée | Fragment lisible |
|---|---|---|
| `87384.wav` | `87384_decoded.png` | `OPENNC{S4FE_` |
| `24354.wav` | `24354_decoded.png` | `ZONE_ANTI_` |
| `09376.wav` | `09376_decoded.png` | `I4}` |

### 3. Recomposition

On concatène les trois fragments dans l'ordre logique (`OPENNC{` … `}`) :

```
OPENNC{S4FE_  +  ZONE_ANTI_  +  I4}
```

soit, en leetspeak, « **SAFE ZONE ANTI IA** » (une zone protégée anti-IA, cohérent avec
KAIROS l'IA hostile du scénario). Le `4` remplace le `A` (comme dans `S4FE`).

Les trois images SSTV portent chacune un fragment, à lire attentivement (leet, `0` et `4`) : `OPENNC{S4FE_` + `Z0NE_4NTI_` + `I4}`. Erreur initiale : lecture `ZONE_ANTI_` (lettres au lieu de `0`/`4`), refusée par la plateforme.

Flag : ``OPENNC{S4FE_Z0NE_4NTI_I4}``

Confiance : **probable** (fragments 1 et 2 très nets ; le 3ᵉ se lit `I4}`). Variante à tester
si refus : ``OPENNC{S4FE_ZONE_ANTI_IA}``.

## Fichiers

- `Ondes.zip` d'origine : `09376.wav`, `24354.wav`, `87384.wav` (copiés ici)
- Images décodées : `87384_decoded.png`, `24354_decoded.png`, `09376_decoded.png`
