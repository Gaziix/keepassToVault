from keepassToVault import KeepassToVault
import re, argparse

# chargement de la DB Keepass
try:
    # manage all parameters that can be implements
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--address", help="Vault URL, if no one is entered, this value is put to https://127.0.0.1:8200.")
    parser.add_argument("-t","--token", help="root token (it will be ask if nothing is insert here)")
    parser.add_argument("-n", "--namespace", help="namespace (for enterprise editions ONLY)")
    parser.add_argument("-k", "--keepass", help="keepass DB directory", required=True)
    parser.add_argument("-i", "--inscription", help="launch the process to register members in Vault", action="store_true")
    parser.add_argument("-r", "--insertionKV", help="insert Key/Values in Vault", action="store_true")
    parser.add_argument("-c", "--check", help="check Vault integrity", action="store_true")
    
    args = parser.parse_args()
    
    regex = r"\w+\.kdbx$"
    if re.search(regex, args.keepass):
        keepass = KeepassToVault(directory=args.keepass, url=args.address, token=args.token, namespace=args.namespace)
        
        if args.inscription:
            keepass.inscription()
            
        if args.insertionKV:
            keepass.insertionKeyValue()
            
        if args.check:
            keepass.checkIntegrity()
    else:
        raise FileNotFoundError
except ValueError as e:
    print(e)
#except FileNotFoundError: 
    # en cas de bug (getpass qui reçoit un mauvais mdp principalement)
#    print("Wrong directory for your .kdbx") 
except KeyboardInterrupt:
    print("You interrupted the program")
