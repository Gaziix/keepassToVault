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

![Capture d’écran du 2023-05-02 16-18-28](https://user-images.githubusercontent.com/100801507/235694307-f44ab1f9-74dc-40f3-8852-09f45b687907.png)
