# Simini
```markdown
<div id="language-selector">
    <select onchange="switchLanguage(this.value)">
        <option value="en">English</option>
        <option value="fr">Français</option>
    </select>
</div>

<div id="content-en">
    # Simini

    Simini is a project aimed at providing a `curses`-based user interface to configure simulation parameters, similar to the `ccmake` tool.

    ## Features

    - Intuitive terminal-based interface.
    - Easy navigation to adjust simulation parameters.
    - Real-time preview of changes.

    ## Prerequisites

    - Python 3.x
    - `curses` library (usually included with Python on Unix systems).

    ## Installation

    Clone this repository and navigate to the directory:

    ```bash
    git clone https://github.com/your-username/simini.git
    cd simini
    ```

    ## Usage

    Launch the interface with the following command:

    ```bash
    python simini.py
    ```

    Navigate through the interface to configure your simulation parameters.

    ## Contribution

    Contributions are welcome! Please submit a pull request or open an issue to report bugs or suggest improvements.

    ## License

    This project is licensed under the [UNLICENCE](LICENSE) license.
</div>

<div id="content-fr" style="display:none;">
    # Simini

    Simini est un projet visant à fournir une interface utilisateur basée sur `curses` pour configurer les paramètres de simulation, similaire à l'outil `ccmake`.

    ## Fonctionnalités

    - Interface intuitive basée sur le terminal.
    - Navigation facile pour ajuster les paramètres de simulation.
    - Aperçu en temps réel des modifications.

    ## Prérequis

    - Python 3.x
    - Bibliothèque `curses` (généralement incluse avec Python sur les systèmes Unix).

    ## Installation

    Clonez ce dépôt et accédez au répertoire :

    ```bash
    git clone https://github.com/your-username/simini.git
    cd simini
    ```

    ## Utilisation

    Lancez l'interface avec la commande suivante :

    ```bash
    python simini.py
    ```

    Naviguez dans l'interface pour configurer vos paramètres de simulation.

    ## Contribution

    Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour signaler des bugs ou suggérer des améliorations.

    ## Licence

    Ce projet est sous licence [UNLICENSE](LICENSE).
</div>

<script>
    function switchLanguage(lang) {
        document.getElementById('content-en').style.display = lang === 'en' ? 'block' : 'none';
        document.getElementById('content-fr').style.display = lang === 'fr' ? 'block' : 'none';
    }
</script>
```
