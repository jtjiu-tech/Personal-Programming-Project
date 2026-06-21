import random
import time
def InputPlainText():     
    PlainText = input("Please enter the plaintext: ")
    while PlainText == "":
        PlainText = input("Please enter the plaintext: ")
    return PlainText

def InputCipherText():     
    CipherText = input("Please enter the ciphertext: ")
    while CipherText == "":
        CipherText = input("Please enter the plaintext: ")
    return CipherText

def InputKey():  
    Key = input("Please enter the key value: ")
    return int(Key)

def Encrypt(PlainText, Key):
    CipherText = ""
    for CharPos in range(0, len(PlainText)):
        Character = PlainText[CharPos]
        CharacterCode = ord(Character)
        if  CharacterCode >= ord("A") and CharacterCode <= ord("Z"):
            CharacterCode = CharacterCode + Key 
            if  CharacterCode > ord("Z"):
                CharacterCode = CharacterCode - 26
        elif CharacterCode >= ord("a") and CharacterCode <= ord("z"):
            CharacterCode = CharacterCode + Key 
            if  CharacterCode > ord("z"):
                CharacterCode = CharacterCode - 26
        CipherText = CipherText + chr(CharacterCode) 

    return CipherText

def LoadPlainText():    
    FileName = input("Enter filename: ")
    if len(FileName) > 0:
        FileHandle = open(FileName)  
        PlainText = FileHandle.read() 
        FileHandle.close() 
    else:
        PlainText = "Error"
 
    return PlainText

def Decrypt(CipherText, Key):
    PlainText = ""
    for CharPos in range(0, len(CipherText)):
        Character = CipherText[CharPos]
        CharacterCode = ord(Character)
        if  CharacterCode >= ord("A") and CharacterCode <= ord("Z"):
            CharacterCode = CharacterCode - Key
            if  CharacterCode < ord("A"):
                CharacterCode = CharacterCode + 26          
                
        PlainText = PlainText + chr(CharacterCode)

    return PlainText

def DisplayMenu():
    print()
    print("K Input Key")
    print("P Input Plaintext")
    print("C Input Ciphertext")
    print("L Load Plaintext")
    print("E Encrypt Plaintext")
    print("D Decrypt Ciphertext")
    print("4 Random Plaintext")
    print("Q Quit")
    print()

def GetRandomPlainText():
    total = []
    new = ""
    words = ["that", "those", "idk", "I", "had" ,"found" ,"it" ,"tucked" ,"inside" ,"his" ,"laptop" ,"case", "the", "one" ,"he" ,"never" ,"let", "me", "touch","because"]
    sentencelength = int(input("How long do you want the plaintext to be? "))
    for i in range(sentencelength):
        randomwords = random.choice(words)
        total.append(randomwords)
    text = total[0]
    total.pop(0)
    result = text[0].upper() + text[1:]
    new = " ".join(total)
    print(result + " " + new + ".")

def shift():

    pass


def Main():

    MenuOption = ""  

    while MenuOption != "Q":
        DisplayMenu()
        MenuOption = input("Enter Option > ").upper()
        if MenuOption == "K":
            Key = InputKey()
        elif MenuOption == "P":
            PlainText = InputPlainText()
        elif MenuOption == "C":
            CipherText = InputCipherText()
        elif MenuOption == "L":
            PlainText = LoadPlainText()
            print("Plaintext is : " + PlainText)
        elif MenuOption == "E":
            CipherText = Encrypt(PlainText, Key)
            print("Ciphertext is : " + CipherText)
        elif MenuOption == "D":
            PlainText = Decrypt(CipherText, Key)
            print("Plaintext is : " + PlainText)
        elif MenuOption == "4":
            Plaintext = GetRandomPlainText()
        else:
            print("That isn't one of the options, Try again. ")
Main()