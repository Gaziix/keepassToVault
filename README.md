# Vault To Keepass

Ce projet va vous permettre de téléverser des données d'une base de données Keepass à un serveur Vault. Plusieurs processus sont possibles. Tout d'abord, vous allez avoir à chaque fois le choix de choisir quels groupes de la base de données du Keepass vous souhaitez utiliser pour votre manipulation. 
Vous avez donc le choix entre : 
 - insérer des données tel que KEY/VALUE (utiliser l'option -r ou --insertionKV).
 - initier de nouveaux profils ayant accès au serveur Vault, en leur attribuant une policy déjà existante (utiliser l'option -i ou --inscription).
 - vérifier l'intégrité des données du Vault par rapport au Keepass (utiliser l'option -c ou --check).

# Install
Make sure you have these packets installed :

    sudo python3 -m pip install hvac
    sudo python3 -m pip install pykeepass
    python3 main.py -k KEEPASS_FILE.kdbx
Download main.py and keepassToVault.py from this repo. Ils sont très simple d'utilisation
## Usage

usage: main.py [-h] [-a ADDRESS] [-t TOKEN] [-n NAMESPACE] -k KEEPASS [-i] [-r] [-c]

options:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Vault URL, if no one is entered, this value is put to https://127.0.0.1:8200.
  -t TOKEN, --token TOKEN
                        root token (it will be ask if nothing is insert here)
  -n NAMESPACE, --namespace NAMESPACE
                        namespace (for enterprise editions ONLY)
  -k KEEPASS, --keepass KEEPASS
                        keepass DB directory
  -i, --inscription     launch the process to register members in Vault
  -r, --insertionKV     insert Key/Values in Vault
  -c, --check           check Vault integrity


