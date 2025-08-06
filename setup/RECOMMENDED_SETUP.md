# Configuration Recommandée pour Hackagou CTF

Ce document décrit les configurations d'environnement recommandées pour participer efficacement à l'épreuve CTF "Hackagou". Nous privilégions deux options principales : Kali Linux (en machine virtuelle ou sur matériel dédié) et WSL (Windows Subsystem for Linux) avec Windows.

## 1. Kali Linux (Recommandé)

Kali Linux est une distribution basée sur Debian, spécialement conçue pour les tests d'intrusion et l'audit de sécurité. Elle est livrée avec une multitude d'outils préinstallés, ce qui en fait un choix idéal pour les CTF.

### Installation

#### Option A : Machine Virtuelle (VirtualBox ou VMware)

1.  **Télécharger Kali Linux :** Rendez-vous sur le site officiel de Kali Linux ([https://www.kali.org/get-kali/#kali-virtual-machines](https://www.kali.org/get-kali/#kali-virtual-machines)) et téléchargez l'image ISO ou une image pré-construite pour VirtualBox/VMware.
2.  **Installer VirtualBox/VMware Workstation Player :** Si vous ne l'avez pas déjà, téléchargez et installez votre logiciel de virtualisation préféré.
    *   VirtualBox : [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)
    *   VMware Workstation Player : [https://www.vmware.com/fr/products/workstation-player/workstation-player-evaluation.html](https://www.vmware.com/fr/products/workstation-player/workstation-player-evaluation.html)
3.  **Créer une nouvelle machine virtuelle :**
    *   Ouvrez VirtualBox/VMware et créez une nouvelle machine virtuelle.
    *   Sélectionnez l'image ISO de Kali Linux ou importez l'image pré-construite.
    *   Allouez au moins 4 Go de RAM et 40 Go d'espace disque.
    *   Configurez la carte réseau en mode "NAT" pour l'accès à Internet et éventuellement en mode "Host-only" ou "Bridge" pour la communication avec d'autres machines virtuelles ou le réseau local si nécessaire.
4.  **Démarrer et installer Kali Linux :** Suivez les instructions d'installation de Kali Linux. Les identifiants par défaut sont généralement `kali`/`kali` ou `root`/`toor` (à changer après l'installation).
5.  **Mettre à jour le système :** Une fois l'installation terminée, ouvrez un terminal et exécutez :
    ```bash
    sudo apt update
    sudo apt full-upgrade -y
    ```
6.  **Installer les Guest Additions (VirtualBox) / VMware Tools (VMware) :** Cela améliorera l'intégration (redimensionnement de l'écran, copier-coller, etc.).

#### Option B : Installation sur Matériel Dédié (Avancé)

Si vous avez un ordinateur de rechange, une installation directe de Kali Linux peut offrir de meilleures performances. Suivez les instructions officielles de Kali pour l'installation sur disque dur.

## 2. WSL (Windows Subsystem for Linux) + Windows

WSL permet d'exécuter un environnement Linux directement sur Windows, offrant un bon compromis entre la commodité de Windows et la puissance des outils Linux.

### Installation

1.  **Activer WSL :** Ouvrez PowerShell en tant qu'administrateur et exécutez :
    ```powershell
    wsl --install
    ```
    Cela installera automatiquement Ubuntu par défaut. Si vous souhaitez une autre distribution (comme Kali Linux), vous pouvez la spécifier :
    ```powershell
    wsl --install -d Kali-Linux
    ```
    Redémarrez votre ordinateur si vous y êtes invité.
2.  **Configurer votre distribution Linux :** Après le redémarrage, votre distribution Linux s'ouvrira. Suivez les instructions pour créer un nom d'utilisateur et un mot de passe.
3.  **Mettre à jour le système :** Ouvrez le terminal de votre distribution WSL et exécutez :
    ```bash
    sudo apt update
    sudo apt full-upgrade -y
    ```
4.  **Installer les outils essentiels :** Bien que WSL n'inclue pas tous les outils de Kali par défaut, vous pouvez installer ceux dont vous avez besoin. Voici quelques exemples :
    ```bash
    sudo apt install nmap wireshark metasploit-framework john the-harvester sqlmap burpsuite -y
    ```
    *Note : Certains outils graphiques peuvent nécessiter un serveur X (comme VcXsrv) pour fonctionner sur Windows.*

## Outils Python

Étant donné que certains membres de l'équipe utilisent Python, assurez-vous d'avoir `pip` et `venv` installés pour gérer les dépendances et les environnements virtuels.

```bash
sudo apt install python3 python3-pip python3-venv -y
```

Pour créer et activer un environnement virtuel :

```bash
python3 -m venv mon_env_ctf
source mon_env_ctf/bin/activate
```

## Recommandations Générales

*   **Mises à jour régulières :** Gardez votre système et vos outils à jour.
*   **Snapshots (VM) :** Prenez des snapshots de votre machine virtuelle avant des changements majeurs ou des CTF pour pouvoir revenir à un état stable.
*   **Espace disque :** Assurez-vous d'avoir suffisamment d'espace disque pour les outils, les captures de trafic et les fichiers de travail.
*   **Connaissance des outils :** Familiarisez-vous avec les outils de base (nmap, netcat, wireshark, burpsuite, etc.) avant le jour J.