import random

def main():
    print("\n-------------------------------------")
    print("==WELCOME TO THE PASSWORD GENERATOR==")
    print("============HERE YOU GO==============")
    print("-------------------------------------")
    uppercase_letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
    lowercase_letters = uppercase_letters.lower()
    digits = "0123456789"
    symbols = "!@#$%^&*()_+-=`/.,"

    upper, lower, nums, syms = True, True, True, True

    all = ""

    if upper:
        all += uppercase_letters
    if lower:
        all += lowercase_letters
    if nums:
        all += digits
    if syms:
        all += symbols

    length = 20
    amount = 10

    print("\n       --------------------")
    for x in range(amount):
        password = "".join(random.sample(all, length))
        print("     >", password)

    print("       --------------------\n")
    print("         here you go !\n")

    u_i = input("do you wanna (Q)uit or continue?       #")

    while u_i.upper() != 'Q':
        print("\n       --------------------")
        for x in range(amount):
            password = "".join(random.sample(all, length))
            print("     >", password)

        print("       --------------------\n")
        print("         here you go !\n")

        u_i = input("do you wanna (Q)uit or continue?       #")

if __name__ == '__main__':
    main()
