import sys
import hashlib
import json
import os
import getpass
import time
import random 
from plyer import notification

class bankSystem:
    def __init__(self):

        # Defining storage files.
        self.FILES = {
            "passwords" : "password_file.json",
            "matrix" : "access_matrix.json",
            "salts" : "passwords_salts.json",
            "balances" : "balances_database.json",
            "phones" : "phone_numbers.json",
            "usersPhones" : "users_phones.json",
        }

        # Check if there are missing system files to create them.
        self.checkInitSystem()

        # Parsing JSON files
        self.passwords = self.loadJson(self.FILES['passwords'])
        self.balances = self.loadJson(self.FILES['balances'])
        self.usersPhones = self.loadJson(self.FILES['usersPhones'])
        self.matrix = self.loadJsonMatrix(self.FILES['matrix'])
        self.salts = self.loadJson(self.FILES['salts'])
        self.validPhones = self.loadJson(self.FILES['phones'])

        self.current_user = None

    def clearScreen(self):
       """ Clear screen after the end of an event. """
       os.system('cls')

    def checkInitSystem(self):
        """ Checks missing systems files and creates the missing ones. """
        # Defining the structure of each data file
        emptyDefaults = {
            "passwords" : {},
            "matrix" : {},
            "salts" : {},
            "balances" : {},
            "usersPhones" : {},
            "phones" : []
        }

        # Iterate on each file to check its existnce
        for key, filename in self.FILES.items():
            if key == "phones":
                continue
            if not os.path.exists(filename):
                print(f"'{filename}' is missing. Creating a new one...\n")
                data = emptyDefaults.get(key,{})
                self.saveJson(filename,data)
        if not os.path.exists(self.FILES["phones"]):
            print(f"'{self.FILES["phones"]}' is missing. Creating a new one...\n")
            self.generatePhoneNumbers(10)
        time.sleep(3)

    def generatePhoneNumbers(self, count = 20, filename = "phone_numbers.json"):
        """ Generate a random list of registered phone numbers. """

        prefixes = ["010","011","012","015"]
        phoneNumberList = []

        print(f"Generating {count} registered phone numbers...\n")
        for i in range(count):
            
            # Generating random number with 8 digits with possible leading zeros
            prefix = random.choice(prefixes)
            rest = f"{random.randint(0,99999999):08}"
            phoneNumberList.append(prefix + rest)

        self.saveJson(self.FILES["phones"], phoneNumberList)
        self.validPhones = phoneNumberList

    # Convert json file to python dictionary.
    def loadJson(self, filename):
        with open(filename, 'r') as f: return json.load(f)

    # Save a dictionary into json file.
    def saveJson(self, filename, data):
        with open(filename, 'w') as f: json.dump(data, f, indent=4)

    # Parses the JSON file and transforms the {User: [List]} structure into {User: {Set}} to optimize permission checks. 
    def loadJsonMatrix(self, filename):
        data = self.loadJson(filename)
        
        resultMap = {}

        for user, allowed_list in data.items():
            converted_set = set(allowed_list)
            resultMap[user] = converted_set

        return resultMap
    
    # Update the access matrix.
    def saveMatrixUpdate(self):
        matrixAsLists = {}

        for user, allowed_set in self.matrix.items():
            converted_list = list(allowed_set)
            matrixAsLists[user] = converted_list
        self.saveJson(self.FILES["matrix"], matrixAsLists)

    def register(self):

        """                                         User Registeration: 
        User enters his registered phone number and receives OTP code for verification 'pop notification for simulation'
        after a success verification, he has to enter a unique username. For password, a salt of 16 bytes hex is generated 
        and added to the password, and save the computed hash of that in the JSON password files. Salts have their own JSON 
        files to be retrieved for user authentication process."""
        
        self.clearScreen()
        print("=== New User Registeration ===\n")

        phoneNumber = input("Enter your registered phone number: ").strip()
    
        if not phoneNumber.isdigit():
            print("ERROR: only numbers are allowed.!\n")
            time.sleep(2)
            return 
        
        if len(phoneNumber) != 11:
            print("ERROR: Phone number should have 11 digits.!\n")
            time.sleep(2)
            return
        
        if phoneNumber not in self.validPhones:
            print("\nERROR: This phone number is not registered in the system!\n")
            time.sleep(2)
            return
        
        if phoneNumber in self.usersPhones.values():
            print("\nError: Unable to process registration for this number.\n")
            time.sleep(2)
            return 
        
        # Generating a random OTP code from 1000 to 9999
        otpCode = str(random.randint(1000,9999))
        print(f"OTP code sent to {phoneNumber}...\n")

        # Structure of the notification message window
        notification.notify(
            title = "Bank System",
            message = f"Your OTP code: {otpCode}",
            timeout = 3)


        userInputOTP = input("Enter the OTP code sent to your phone number: ")
        if userInputOTP != otpCode:
            print("Invalid OTP! registeration aborted!...\n")
            time.sleep(2)
            return 
        
        print("Success OTP Verification!\n")

        username = input("Username: ").strip()
        if not username:
            print("\nERROR: Username can not be empty.!\n")
            time.sleep(2)
            return
        if username in self.passwords:
            print("\nERROR: Username already exists.!\n")
            time.sleep(2)
            return        
        password = getpass.getpass("password: ").strip()
        if not password:
            print("\nERROR: Password cannot be empty!\n")
            time.sleep(2)
            return        
        
        # Generate a random 16-hex salt number 
        salt = os.urandom(16).hex()

        saltedPassword = password + salt
        hashedPassword = hashlib.sha256(saltedPassword.encode()).hexdigest()

        self.salts[username] = salt
        self.saveJson(self.FILES["salts"], self.salts)

        self.passwords[username] = hashedPassword
        self.saveJson(self.FILES["passwords"], self.passwords)

        self.balances[username] = float(random.randint(100, 5000))
        self.saveJson(self.FILES["balances"],self.balances)

        self.usersPhones[username] = phoneNumber
        self.saveJson(self.FILES["usersPhones"],self.usersPhones)

        self.matrix[username] = {username}
        self.saveMatrixUpdate()

        print("Account created successfully!\n")
        time.sleep(2)

    
    # User login.
    def login(self):
        self.clearScreen()
        print("=== BANK SYSTEM ===\n")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        if username not in self.passwords:
            print("\nLogin Failed!: Invalid Credentials.\n")
            time.sleep(2)
            return False
        
        userSalt = self.salts[username]
        saltedInput = password + userSalt

        # hash the input password and compare it with the preserved hashed one.
        hashedInput = hashlib.sha256(saltedInput.encode()).hexdigest()

        if self.passwords[username] == hashedInput:
            self.current_user = username
            print("\nLogin Success.!\n\n")
            return True
        else:
            print("\nLogin Failed!: Invalid Credentials.\n")
            time.sleep(2)
            return False
    # Showing the current user's balance.
    def viewSelfBalance(self):
        self.clearScreen()
        print(f"\nYour balance is ${self.balances[self.current_user]:.2f}\n")
        input("Strike enter key to go back...\n")
    
    def viewBalance(self):
        self.clearScreen()
        target = input("View balance of user: ").strip()

        if target not in self.balances:
            print("\nACCESS DENIED!\n")
            time.sleep(2)
            return 
        
        if self.current_user in self.matrix.get(target, set()):
            print(f"\nBalance of {target} is ${self.balances[target]:.2f}\n")
            input("Strike enter key to go back...\n")
        else:
            print("\nACCESS DENIED!\n")
            time.sleep(2)
        
    def grantAccess(self):
        self.clearScreen()
        target = input("Enter the username you want to grant access to: ")

        if target not in self.balances:
            print("\nERROR: Unable to process access for that user.!\n")
            time.sleep(2)
            return
        
        if target in self.matrix[self.current_user]:
            print("\nThis user has access already.!\n")
            time.sleep(2)
            return
        
        self.matrix[self.current_user].add(target)
        self.saveMatrixUpdate()

        print("\nAccess Granted!\n")
        time.sleep(2)
    
    def revokeAccess(self):
        self.clearScreen()
        target = input("Enter the username you want to revoke access from: ")

        if target == self.current_user:
            print("\nERROR: You can't block yourself!\n")
            time.sleep(2)
            return
        
        if target in self.matrix[self.current_user]:
            self.matrix[self.current_user].remove(target)
            self.saveMatrixUpdate()
            print(f"Access Revoked from {target}!\n")
        else:
            print(f"\n{target} already doesn't have access\n")
        time.sleep(2)
        
    def startSystem(self):
        while True:
            if not self.current_user:
                self.clearScreen()
                print("=== Welcome to Bank System! ===\n")
                print("1- Login\n")
                print("2- Register New User\n")
                print("3- Exit\n")

                choice = input("Select: ")
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.register()
                elif choice == '3':
                    sys.exit()
                continue

            self.clearScreen()
            print(f"Current user : {self.current_user}\n")
            print("1- View Your Balance\n")
            print("2- View Others' Balance\n")
            print("3- Grant Access\n")
            print("4- Revoke Access\n")
            print("5- Logout\n")
            print("6- Exit\n")
            
            choice = input("Select: ")
            print("\n")
            if choice == '1':
                self.viewSelfBalance()
            elif choice == '2':
                self.viewBalance()
            elif choice == '3':
                self.grantAccess()
            elif choice == '4':
                self.revokeAccess()
            elif choice == '5':
                self.current_user = None
                print("Logging out...\n")
                time.sleep(2)
            elif choice == '6':
                print("Exiting...\n")
                time.sleep(2)
                sys.exit()

app = bankSystem()
app.startSystem()