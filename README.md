# ♟️ Crimson Nexus

 Jeu d'échecs moderne en Python avec interface graphique, mode local contre IA et multijoueur en ligne.

---

## 🚀 Objectifs du projet

Crimson Nexus est un **jeu d’échecs complet** développé en Python avec Pygame. Il propose deux modes :

- **Solo contre une IA rapide**, avec une logique stratégique de base
- **Multijoueur en ligne**, avec système de salon hôte/client (connexion par IP)

Le jeu implémente **toutes les règles officielles** : roque, prise en passant, promotion, pat, échec et mat.

---

## 🧩 Fonctionnalités

- 🎮 Interface graphique fluide et responsive (Pygame)
- 💡 Mise en évidence des coups possibles
- 📜 Historique des coups joués
- ♻️ Écran de fin avec options "Rejouer" ou "Retour menu"
- 🔌 Connexion réseau TCP/IP hôte/client pour jouer à distance
- 🧠 IA réactive avec priorisation des captures et coups "safe"

---

## 🛠️ Installation et lancement

### 🔧 Dépendances

Crimson Nexus fonctionne avec Python ≥ 3.10.  
Installez les dépendances avec :

pip install pygame pygame_textinput



###▶️ Lancer le jeu

Assurez-vous que votre terminal pointe vers le dossier racine, puis exécutez :

python main.py

###🗂️ Structure du projet

Crimson Nexus/
 main.py                  # Point d’entrée principal du jeu
 README.md                # Ce fichier
ui/                      # Interface utilisateur (menus, graphismes, boucles de jeu)
 menu.py              # Menu principal
 game_loop.py         # Partie contre l'IA
 network_game_loop.py # Partie multijoueur en ligne
 lobby_host.py        # Interface de création de salon
 lobby_client.py      # Interface pour rejoindre un salon
 draw.py              # Fonctions d'affichage (plateau, pièces, historique…)

core/                    # Cœur logique du jeu d’échecs
 board.py             # Représentation du plateau et logique de partie
 move.py              # Représentation des coups
 pieces.py            # Définition de chaque type de pièce
 rules.py             # Règles spéciales (roque, échec, etc.)

ai/
 base_ai.py           # Intelligence artificielle simple (priorité aux captures)

 network/                 # Gestion de la communication réseau
  network.py           # Serveur et client TCP
  lobby_host.py        # Création de salon (UI)
  lobby_client.py      # Connexion à un salon (UI)
  
 assets/                  # Dossier contenant les icônes et les pièces d’échecs




## ✨ Points techniques notables

-  L’IA utilise un thread Python pour réfléchir sans bloquer l’affichage

-  La communication réseau passe par un protocole TCP custom avec pickle

-  Le projet respecte une séparation claire entre logique (core), affichage (ui) et réseau
