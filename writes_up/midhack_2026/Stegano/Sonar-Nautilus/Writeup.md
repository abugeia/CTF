# Le Sonar du Nautilus

Catégorie : Stégano — Points : 250 (dynamique) — Auteur : (MidHack 2026)

## Énoncé

Dans les ruines submergées de la cité de Kelot, l'équipage a récupéré une capsule
étanche du sous-marin à vapeur *Nautilus-IV*, contenant un fichier journal
`sonar.log` : l'historique des relevés d'un sonar actif à balayage sectoriel le
long d'une épave métallique.

Mission : reconstruire la carte 2D de l'épave détectée par le sonar pour lire le
message secret (le flag) qui y est gravé.

### Format des données (`sonar.log`)

```
t={t} | sub_pos={x},{y} | sub_yaw={yaw} | env={depth},{temp},{salinity} | ping={angle},{time},{intensity}
```

### Modèle physique

1. Vitesse du son en eau de mer :
   `c = 1449.2 + 4.6T − 0.055T² + 0.00029T³ + (1.34 − 0.01T)(S − 35) + 0.016z`
2. Distance de l'obstacle : aller-retour → `r = c·Δt / 2`
3. Coordonnées globales :
   `X = X_sub + r·cos(φ + θ)` ; `Y = Y_sub + r·sin(φ + θ)`

Filtrage : ne conserver que les échos d'**intensité ≥ 150**. Le flag est
légèrement déformé par des courants oscillants (rides), illisible par OCR mais
lisible à l'œil.

## Résolution

### 1. Reconstruction

Pour chaque ping avec `intensity ≥ 150` : calcul de `c`, puis `r = c·Δt/2`, puis
`(X, Y)`. On obtient ~345 points (voir `solve.py`).

```python
c = 1449.2 + 4.6*T - 0.055*T**2 + 0.00029*T**3 + (1.34-0.01*T)*(S-35) + 0.016*z
r = c*dt/2.0
X = sx + r*math.cos(yaw+angle)
Y = sy + r*math.sin(yaw+angle)
```

Le nuage brut (`nuage_brut.png`) montre déjà un texte ondulé sur ~111 m de large
et ~6 m de haut.

### 2. Retrait de la distorsion et orientation

- Les points ondulent selon X (rides marines) : sinusoïde d'axe X de période
  ~25 m. On ajuste `A·sin(ωX+φ)` sur la médiane de Y par tranches et on la
  soustrait, ce qui redresse le texte.
- Les lettres apparaissent **verticalement inversées** (les « N » ressemblent à
  « И ») : il faut inverser l'axe Y (`invert_yaxis`).

Le tracé final (`reconstruction.png`) est parfaitement lisible :

```
OPENNC{PUnk_0c3an_S0n4r_76}
```

Vérifié caractère par caractère par zoom sur les segments (`PUnk` / `_0c3an_` /
`S0n4r_76}`).

## Flag

Confiance : **sûr** (lecture nette après redressement).

Flag : ``OPENNC{PUnk_0c3an_S0n4r_76}``
