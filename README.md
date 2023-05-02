# Keepass to Vault

This project will allow you to upload data from a Keepass database to a Vault server. Several processes are possible. First of all, you will have the choice to select which groups of the Keepass database you want to use for your manipulation. 
You have the choice between : 
 - insert data such as KEY/VALUE (use the -r or --insertionKV option).
 - initiate new profiles with access to the Vault server, by assigning them an existing policy (use the -i or --inscription option).
 - verify the integrity of the Vault data against the Keepass (use the -c or --check option).

# Install
Make sure you have these packets installed :

    sudo python3 -m pip install hvac
    sudo python3 -m pip install pykeepass
    python3 main.py -k KEEPASS_FILE.kdbx
Download main.py and keepassToVault.py from this repo. They are very easy to use.
## Usage

![Capture d’écran du 2023-05-02 16-18-28](https://user-images.githubusercontent.com/100801507/235694307-f44ab1f9-74dc-40f3-8852-09f45b687907.png)
