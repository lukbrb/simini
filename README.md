# Simini

1. [Version française](#français)
2. [English Version](#english)


## English

Simini is a project aimed at providing a `curses`-based user interface to configure simulation parameters.

## Features

- Intuitive terminal-based interface.
- Easy navigation to adjust simulation parameters.
- Real-time preview of changes.

## Prerequisites

- Python 3.x
- `curses` library (included with Python on Unix systems).

## Installation

Clone this repository and navigate to the directory:

```bash
git clone https://github.com/your-username/simini.git
cd simini
```

## Usage

Create a `config.py` file in the same directory, setting up the parameters your simulations need, and their ranges of validity. The `config.py` file for `fv2d` is given as an example.
Launch the interface with the following command:

```bash
python simini.py
```

Navigate through the interface to configure your simulation parameters for a given problem. Once ready, you can generate the `.ini` file by typing `g`. Exit the program with `q`. 

## Contribution

Contributions are welcome! Please submit a pull request or open an issue to report bugs or suggest improvements.

## License

This project is licensed under the [UNLICENCE](./LICENSE.md) license.

## Français

Simini est un projet visant à fournir une interface utilisateur basée sur `curses` pour configurer les paramètres de simulation.

## Prérequis

- Python 3.x
- Bibliothèque `curses` (incluse avec Python sur les systèmes Unix).

## Installation

Clonez ce dépôt et accédez au dossier :

```bash
git clone https://github.com/your-username/simini.git
cd simini
```

## Utilisation

Il est nécessaire de créer un fichier `config.py` dans le même dossier, où sont spécifiés les paramètres disponibles de votre simulation. Leur intervalle de validité peut également être spécifié.
Ce répertoire contient le fichier `config.py` de `fv2d` à titre d'exemple.
Lancez l'interface avec la commande suivante :

```bash
python simini.py
```

Naviguez dans l'interface pour configurer vos paramètres de simulation pour un problème donné. Une fois prêt, tapez `g` pour générer le fichier `.ini` spécifique à votre problème. Quittez le programme en tapant `q`.

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour signaler des bugs ou suggérer des améliorations.

## Licence

Ce projet est sous licence [UNLICENSE](./LICENSE.md).
