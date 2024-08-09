length = int(input("Enter the length of the password: "))
import random
import string
def passgen(length, digits = True, symbols = True):

    pospwd = ''
    letters = string.ascii_letters
    pospwd += letters
    if digits:
        num = string.digits
        pospwd += num
    if symbols:
        special = string.punctuation   
        pospwd += special 
    
    

    password = ''


    while len(password) < length:
        
        password += random.choice(pospwd)
    return(password)
print(passgen(length))