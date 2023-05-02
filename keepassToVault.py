import re, hvac
from pykeepass import PyKeePass
from getpass import getpass

# Prochain objectif (j'ai un prog qui passe tout vault, j'ai besoin de m'auth de maniere secure, comment faire (use HVAC)):
# - expliquer le fait de mettre le serveur en mode dev, expliquer pourquoi des fois c'est bien, des fois pas bien au début, proposer un vault dev ou vault enterprise avec namespace
# - FINAL OBJECTIF : mettre le projet sur Github
# - mettre en place des update possible côté Vault OU Keepass, et màj de l'autre côté en conséquence
# - créer une policies on choisissant direct quels users pourront l'avoir

class KeepassToVault:
    """
        Class: 
            Allows you to move a database from Keepass to Vault without data loss, securely and quickly.
    
        Parameters:
            - liste_groupe (list): list of groupe associate with title
            - whole_info (list) : the entire info about all groups in Keepass DB that have been choose
            - list_role (list): the whole roles in Keepass DB that need to be move to Vault
            - register_insc (list) : a remember of title that have been register with the policies associate
            - exist (boolean) : if the user we handle is already existing
            - kp (PyKeePass) : our instance of Keepass DB in Python
            - url (str) : the Vault path
            - token (str) : Vault token use to create our vault client to manage it
    """
    def __init__(self, directory, url="http://127.0.0.1:8200", token="root", namespace=""):
        self.liste_groupe = []
        self.list_role = []
        self.whole_info = []
        self.register_insc = []
        self.exist = False
        self.namespace = namespace
        
        # creation of the connection between python and the Keepass DB, a password will be asked at the start
        self.kp = PyKeePass(directory, getpass("Enter your Keepass password : "))
        
        # storing connections data to create the next vault client
        self.url = url
        self.token = token
        
        self.client = None
        
    def main_test(self):
        print(self.url)
        print(self.token)
        
    def authenticate_vault(self, url, token=None, namespace=None):
        """
        This function is used to authenticate a user to the Vault.

        Parameters:
            url (str): The URL of the Vault instance.
            token (str): The authentication token to use. If not specified, the function will prompt the user to enter the token.

        Return:
            client (hvac.Client): An hvac.Client that has been successfully authenticated.
        """
        if not token:
            # ask the user to enter the token
            token = getpass("Saisissez votre token Vault : ")

        # create a hvac.client with the specified URL and token
        client = hvac.Client(url=url, token=token, namespace=namespace)

        # verify that the client is successfully authenticated
        if not client.is_authenticated():
            raise ValueError("L'authentification avec Vault a échoué. Veuillez vérifier votre token et l'URL de l'instance Vault.")

        return client
        
    def defineVersion(self, namespace=""):
        """
        Defines the version of Vault and creates a Vault client for interaction.
        
        Parameters:
            - namespace (optional): enterprise namespace if the version of Vault is Enterprise
        
        Returns:
            - client: object of class hvac.v1.Client that allows interaction with Vault
        
        """
    
        # defines the version and allows you to directly create a Vault client on which you will then interact
        entry = ""
        
        while entry != "1" and entry != "2":
            entry = str(input("Which version of Vault do you have ? FREE(TAPE 1) OR ENTERPRISE(TAPE 2) : "))
            
        if entry == "1":
            # setup client to have the connection to our Vault
            return self.authenticate_vault(self.url, token=self.token)
            
        else:
            tmp = True
            
            while tmp or namespace == "":
                namespace = str(input("What is your enterprise namespace you want to work in ? "))
                a = ""
                
                while a != "y" or a != "n":
                    a = input("Are you sure that namespace={} is the enterprise namespace you want to work in ? (y/n)".format(namespace))
                    a = a.lower()
                    
                if a == "y":
                    tmp = False
                    
            # setup client to have the connection to our Vault
            return self.authenticate_vault(self.url, token=self.token, namespace=namespace)
        
    def fillRoles(self, groupe):
        """
        Allows you to efficiently link groups and titles together in the self.list_role variable of the class. 
        It browses the entries of the group given as parameter, retrieves the last part of the entry corresponding to the title, 
        and adds a dictionary containing the group and title to the list of roles.

        Parameters:
            - group: an object containing the group entries to link with titles.

        Returns:
            Modifies the self.list_role variable of the class.
        """
        # allows us to efficiently link groups and titles together within our class in the variable self.liste_role
        for i in groupe.entries:
            i = str(i).split(" ")[1].split("/")[-1:]
            self.list_role.append({"groupe": groupe, "title": i[0]})
    
    def choseGroups(self, kp_list, self_liste):
        """
        This function is used to choose the groups that will be implemented in Vault.

        Parameters:
            - kp_list (list): a list containing the names of the groups to be selected
            - self_list (list): a list of dictionaries containing the names and groups previously selected

        Returns:
            - list: a list of dictionaries containing the previously selected names and groups, and the newly added values.
        """
        # use to chose the groups values that will be implements in Vault
        a, already_in, j = kp_list, False, 2
        a.pop(0)
        print("{}\n1 : All".format(a))
        
        for j, i in enumerate(a):
            print(j+2, ":", i)
            
        entry = -1
        
        while entry > len(a) or entry <= 0:
            entry = int(input("Which one would you want to add ? : "))
            
        expression_reguliere = r'"(.*?)"'
        if entry > 0 and entry <= len(a) + 1:
            
            if entry == 1:
                
                for i in a:
                    res = re.findall(expression_reguliere, str(i))
                    res = res[0]
                    
                    for j in self_liste:
                        
                        if res in j:
                            already_in = True
                            
                    if already_in:
                        print("(",res,") is already in the list.")
                        already_in = False
                        
                    else:
                        self_liste.append({"name" : res, "groupe" : i})
                print(self_liste)
                
            else:
                entry -= 2
                res = re.findall(expression_reguliere, str(a[entry]))
                res = res[0]
                
                for i in self_liste:
                    
                    if res in i:
                        already_in = True
                        
                if already_in:
                    print("({}) is already in the list.".format(res))
                    already_in = False
                    
                else:
                    self_liste.append({"name" : res, "groupe" : a[entry]})
                    
                    print(self_liste)
                b = "g"
                
                while b.lower() != "y"  and b.lower() != "" and b.lower() != "n":
                    b = input("Do u want to add an other one ? y/n: ")
                    
                if b.lower() == "y" or b.lower() == "":
                    self.choseGroups(kp_list, self_liste)
        
    def add_entry(self, name_role, name_grp):
        """
        Adds entries for each role in the whole_info variable.
        
        Parameters:
            - name_role (str): Name of the role to add.
            - name_grp (str): Name of the group to add the role to.
            
        Returns:
            Modifies the self.whole_info attribute to give it the full information needed.
        """
        # addition of inputs for each role in whole_info variable
        entry, i = self.kp.find_entries_by_title(name_role), 0
        
        while i < len(entry):
            new_entry = {"groupe" : name_grp, "title" : entry[i].title, "username": entry[i].username, "password":entry[i].password}
            
            if new_entry in self.whole_info:
                pass
            else:
                self.whole_info.append(new_entry)
            i+=1

    def each_role_entry(self, dic_grp):
        """
        Retrieves the input information for each role in the group passed in parameter
        and stores it in the variable whole_info.

        Parameters:
            - dic_grp (dict): Dictionary containing the group information to be processed.
        """
        # set up the whole list of tags to fetch
        self.list_role.clear()
        self.fillRoles(dic_grp["groupe"]) # function to fill the role list of the group in question
        
        for i in self.list_role:
            self.add_entry(i["title"], dic_grp["name"])
    
    def each_group_entry(self):
        """
        
        Allow to chose the group you want to implement in Vault, and also associate them with titles.
        
        """
        # set up the entire list of Keepass groups that are to be integrated into the Vault
        self.choseGroups(self.kp.groups, self.liste_groupe)
        
        for i in self.liste_groupe:
            self.each_role_entry(i)
            
    def verifyRegister(self, title):
        """
        Checks if the title passed as parameter is already registered in the list self.register_insc.

        Parameters:
            title (str): The title to check.

        Returns:
            - tmp (boolean) : indicates if the title has been found or not in the list self.register_insc. 
            - policy (str) : contains the policy associated with the title to the title (if the title is found in the list).
        """
        # Allows to verify if the title in param is already register in the self.register_insc list
        tmp, policy = False, ""
        
        for t in self.register_insc:
            if t[0] == title:
                tmp = True
                policy = t[1]
        
        return tmp, policy
            
    ####################################
    # Inserting Keepass users to Vault #
    ####################################
    
    def inscription(self):
        """
        This method writes Keepass usernames and passwords to Vault.
        The associated Vault policies can be chosen by the user or retrieved from previously saved policies. 
        previously saved policies. Pairs with the same titles will receive the same policies.
        """
        # start writing user/mdp to the DB Vault with a choice of policies that can be associate with
        # couples with the same titles will receive the same policies
        if self.client == None:
            self.client = self.defineVersion(self.namespace)
        if self.client.is_authenticated() and self.client.seal_status["sealed"] == False:
            self.each_group_entry()
            # check if userpass method is enabled
            if 'userpass/' not in self.client.sys.list_auth_methods():
                self.client.sys.enable_auth_method('userpass')
            i = 0
            while i < len(self.whole_info):
                # add a way to define the policy for a title, or a way to chose the policy for a specific title
                policies = self.client.sys.list_policies()
                verify_registered, policy = self.verifyRegister(self.whole_info[i]["title"])
                
                if verify_registered:
                    # if the policies has already been chose before (we find this info in self.register_insc)
                    self.client.auth.userpass.create_or_update_user(username=self.whole_info[i]["username"], password=self.whole_info[i]["password"], policies=policy)
                else:
                    
                    # print policies names
                    j = 1
                    for policy in policies['policies']:
                        print(j , " : ", policy)
                    entry = 0
                    # way to chose a policies of a title
                    while type(entry) != int or entry > len(policies['policies']) or entry < 1:
                        entry = int(input("Which one do you want to add to "+self.whole_info[i]["title"]+ " ?"))
                    self.client.auth.userpass.create_or_update_user(username=self.whole_info[i]["username"], password=self.whole_info[i]["password"], policies=policies['policies'][entry-1])
                    self.register_insc.append((self.whole_info[i]["title"], policies['policies'][entry-1]))
                    
                i+=1
                
            print("Keepass's user/passwd have been written in Vault DB")
            
        elif self.client.is_authenticated() == False:
            print("You are not authenticated.")
            self.client = self.defineVersion(self.namespace)
            self.inscription()
            
        else: 
            print("Vault is sealed and you are not authenticated.")
            print(self.client.is_authenticated())
        
    ######################################
    # Inserting key/value pairs in Vault #
    ######################################
    
    def insertionKeyValue(self):
        """
        Starts writing key/value pairs to the DB Vault and deletes any files that may have been created during the program's intervention.
        """
        if self.client == None:
            self.client = self.defineVersion(self.namespace)
        # start writing key/value pairs to the DB Vault
        if self.client.is_authenticated() and self.client.seal_status["sealed"] == False:
            self.each_group_entry()
            i = 0
            
            while i < len(self.whole_info):
                # verification of the existence of the title in Vault
                
                if self.checkExistence(self.whole_info[i]["title"], self.whole_info[i]["username"], self.whole_info[i]["groupe"]):
                    self.whole_info[i]["title"] = self.existenceRemediation(self.whole_info[i]["title"], self.whole_info[i]["username"], self.whole_info[i]["groupe"])
                
                if self.exist == False:
                    
                    # data to insert in kv Vault
                    data = {
                        'user': self.whole_info[i]["username"],
                        'password': self.whole_info[i]["password"],
                    }

                    # allows to write in secret folder the secret, with his own path (group + title)
                    self.client.secrets.kv.v2.create_or_update_secret(
                        path=self.whole_info[i]["groupe"] +"/" +self.whole_info[i]["title"],
                        secret=data
                    )

                    i+=1
                    
                else:
                    self.exist = False
                    self.writeErrorFile("This value : title=" + self.whole_info[i]["title"]+ " , username="+ self.whole_info[i]["username"]+ " exists in the DB Vault. \n")
                    i+=1
                    
            print("Keepass's keys/values have been written in Vault DB")
            
        elif self.client.is_authenticated() == False:
            print("You are not authenticated.")
            self.client = self.defineVersion(self.namespace)
            self.insertionKeyValue()
            
        else: 
            print("Vault is sealed and you are not authenticated.")
        
    def checkExistence(self, title, user, groupe):
        """
        Check if a given title exists in the key/value database in the specified group.
        
        Parameters:
            - title (str): Title to search for.
            - user (str): Username associated with the title.
            - groupe (str): Group in which to search for the title.
            
        Returns:
            - boolean: True if the title exists in the group, False otherwise.
        """
        # checks for the existence of a title in the DB Vault key/value
        if self.client == None:
            self.client = self.defineVersion(self.namespace)
        tmp = True
        
        try:
            list_response = self.client.secrets.kv.v2.list_secrets(
                path=groupe,
            )
            result = list_response["data"]["keys"]
            
            if title in result:
                self.exist = self.checkExistenceUser(user, groupe+"/"+title)
                tmp = True
                
            else:
                tmp = False
            return tmp
        
        except hvac.exceptions.InvalidPath as e:
            return False
    
    def checkExistenceUser(self, user, title):
        """
        Checks if the user exists in the specified title path.

        Parameters:
            - user (str): the user name to look up in the secret.
            - title (str): the path to the secret to read.

        Returns:
            - boolean: True if the username matches the secret, False otherwise.
        """
        # Verify if the user exists in the path title
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=title
        )["data"]["data"]["user"]
        return user == secret
    
    def existenceRemediation(self, title, user, groupe):
        """
        If the given title already exists in the Vault, this function returns a new title that is different from the existing one.

        Parameters:
            - title (str): The original title to check for existence.
            - user (str): The username for which the title is checked.
            - groupe (str): The group under which the title is checked.

        Returns:
            - str: A new title that is different from the existing one.
        """
        # si le titre existe déjà dans la base Vault, on fait tout pour le modifier et avoir un titre différent
        remede, i = title, 1
        
        while self.checkExistence(remede, user, groupe) and self.exist == False:
            remede = title + "_{0}".format(i)
            i+=1
            
        return remede
    
    def writeErrorFile(self, string):
        """
        Writes the string `string` to a log file named "logs_error.log".

        Parameters:
            - string (str): The string to write to the log file.
        """
        # it allows us to have logs about our execute, any error will be reported in this file
        with open('logs_error.log', 'w+') as fichier:
            fichier.write(str(string))
        
    #####################
    # Data verification #
    #####################
    
    def checkIntegrity(self):
        """
        Allows to check the integrity of the Vault's data that have been moved from the Keepass database.
        
        Returns:
            - bool: True if all secrets in the Vault match the corresponding information in the `whole_info` list, False otherwise.
        """
        # allows to check the integrity of the Vault's data that have been moved from keepass DB
        i, tmp = 0, True
        
        if self.client.is_authenticated() and self.client.seal_status["sealed"] == False and len(self.whole_info) != 0:
            
            while i < len(self.whole_info):
                secret = self.client.secrets.kv.v2.read_secret_version(
                    path= self.whole_info[i]["groupe"]+"/"+ self.whole_info[i]["title"]
                )["data"]["data"]
                user = secret["user"]
                passwd = secret["password"]
                
                if user == self.whole_info[i]["username"] and passwd == self.whole_info[i]["password"]:
                    pass
                else:
                    tmp = False
                i+=1
                
        elif self.client.is_authenticated() == False:
            
            self.client = self.defineVersion(self.namespace)
            tmp = self.checkIntegrity()
            print("You are not authenticated.")
            
        else: 
            print("Vault is sealed and you are not authenticated.")
            
        return tmp
    