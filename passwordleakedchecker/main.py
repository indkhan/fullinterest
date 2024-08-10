import requests
import hashlib


def get_password(hashedpassword):
    leak = requests.get(f"https://api.pwnedpasswords.com/range/{hashedpassword[:5]}")
    numandpass = leak.text
    lines = numandpass.splitlines()
    lst = []
    for line in lines:
        lst.append(line)
    return lst


def times(password, hashedpassword, lst):
    for line in lst:
        che = line.split(":")
        if hashedpassword[5:] == che[0]:
            return f"Your password {password} has been leaked {che[1]} times."


def out(yesor, password):
    if yesor:
        return yesor
    else:
        return f"Your password {password} has not been leaked"


def mainf(password):
    hashedpassword = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    allpass = get_password(hashedpassword)
    sele = times(password, hashedpassword, allpass)

    return out(sele, password)


if __name__ == "__main__":
    password = input("Enter your password:     ")
    print(mainf(password))
