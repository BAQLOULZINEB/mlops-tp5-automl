# Modele manuel ou modele AutoML ? (TP05)

| Critere                    | Manuel (rf 500/16)  | AutoML (FLAML 90 s)      |
|----------------------------|---------------------|--------------------------|
| Famille de modele          | foret aleatoire     | xgboost (XGBClassifier)  |
| F1 sur le jeu de test      | 0.8669              | 0.8582                   |
| Temps de recherche machine | 2.0 s (un seul fit) | 90.4 s                   |
| Temps humain (estimation)  | ~1 h (essais TP2)   | ~5 min                   |
| Latence mediane (ms)       | 52.2 / 46.4         | 14.5 / 15.6              |
| Latence p95 (ms)           | 94.3 / 63.5         | 16.2 / 17.0              |
| Taille du fichier (Mo)     | 13.37               | 0.29                     |
| Explicabilite              | importance des variables, 500 arbres de profondeur 16 (lourd a lire) | importance des variables, 333 arbres a 4 feuilles max (plus simples) ; config dans le journal |

Mesures : 200 appels apres 10 appels d'echauffement, deux series par service, poste local Windows.

## Decision (5 lignes) : quel modele mettre en production, et pourquoi ?

Je mettrais en production le modele **AutoML (xgboost)**.
Son F1 (0.8582) est a moins de 0.01 du manuel (0.8669), un ecart d'un ou deux cas sur 134 fraudes, non significatif.
Il est en revanche environ **3 fois plus rapide** (mediane ~15 ms contre ~50 ms) et surtout beaucoup plus stable (p95 ~17 ms contre 63-94 ms).
Il est **46 fois plus leger** (0.29 Mo contre 13.4 Mo) : image Docker plus petite, chargement plus rapide, moins de memoire.
Point de vigilance : il est sauvegarde en cloudpickle (pas skops) ; on garde le manuel en version de repli dans le registre, un simple deplacement d'alias suffit pour revenir en arriere.
