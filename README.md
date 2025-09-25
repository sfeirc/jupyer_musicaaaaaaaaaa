#  Synthétiseur Piano Virtuel

Un synthétiseur piano virtuel interactif créé avec Python et Jupyter Notebook pour des ateliers de programmation musicale.

##  Objectif

Ce projet permet d'apprendre la programmation audio en temps réel en construisant étape par étape un piano virtuel contrôlé par clavier.

##  Fonctionnalités

- **Piano virtuel** : 13 notes (Do4 à Do5) contrôlées par clavier
- **Génération audio** : Ondes sinusoïdales en temps réel
- **Multi-notes** : Possibilité de jouer plusieurs notes simultanément
- **Interface clavier** : Mapping intuitif des touches

## 🎮 Contrôles

| Touche | Note | Touche | Note |
|--------|------|--------|------|
| `q` | Do | `h` | La |
| `z` | Do# | `u` | La# |
| `s` | Ré | `j` | Si |
| `e` | Ré# | `k` | Do2 |
| `d` | Mi | | |
| `f` | Fa | | |
| `t` | Fa# | | |
| `g` | Sol | | |
| `y` | Sol# | | |

- **ESC** : Quitter le programme

##  Installation

### Prérequis
- Python 3.8+
- PIP

### Installation des dépendances

```bash
pip install numpy sounddevice pynput matplotlib
```

## 📚 Utilisation

### Version Notebook

1. Ouvrez `synthétiseur_piano_virtuel.ipynb` dans Jupyter
2. Suivez les missions étape par étape :
   - **Mission 1** : Calcul des fréquences musicales
   - **Mission 2** : Génération d'ondes sinusoïdales
   - **Mission 3** : Système d'oscillateurs multi-notes
   - **Mission 4** : Interface clavier
   - **Assemblage** : Synthétiseur complet
3. Exécutez la dernière cellule pour lancer le piano


##  Théorie Musicale

Le synthétiseur utilise la formule du tempérament égal :

```
f = f₀ × 2^(n/12)
```

Où :
- `f` = fréquence de la note
- `f₀` = fréquence de référence (La4 = 440 Hz)
- `n` = nombre de semitons par rapport à la note de référence

##  Architecture Technique

- **Génération audio** : `sounddevice` pour l'audio en temps réel
- **Interface clavier** : `pynput` pour la détection des touches
- **Calculs numériques** : `numpy` pour la génération d'ondes
- **Threading** : Gestion des oscillateurs avec des verrous

## 📖 Structure du Projet

```
├── synthétiseur_piano_virtuel.ipynb  # Notebook Jupyter
├── README.md                         # Ce fichier
└── LICENSE                           # Licence MIT
```

## 🎓 Pratique

Ce projet est conçu pour l'apprentissage :

1. **Théorie musicale** : Comprendre les mathématiques derrière la musique
2. **Programmation audio** : Génération de signaux numériques
3. **Temps réel** : Gestion des flux audio et des événements



Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
