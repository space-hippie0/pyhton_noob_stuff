from PIL import Image
import random
import os

LOGFILE = "logfile.txt"
HZNt = "----------------------------------------------"


def addPostName(filename, postfix):
    name, ext = os.path.splitext(filename)
    return f"{name}{postfix}{ext}"


def logEncryption(filename, key):
    with open(LOGFILE, "a") as log_file:
        log_file.write(f"{filename}, {key}\n")


def encryptImage(filename: str) -> int:
    with Image.open(filename) as image:
        key = random.randint(1, 1000)
        random.seed(key)

        pixels = image.load()

        for x in range(image.size[0]):
            for y in range(image.size[1]):
                pixel = pixels[x, y]
                pixels[x, y] = (
                    (pixel[0] + random.randint(0, 255)) % 256,
                    (pixel[1] + random.randint(0, 255)) % 256,
                    (pixel[2] + random.randint(0, 255)) % 256
                )
        encrypted_filename = addPostName(filename, "-e")
        image.save(encrypted_filename)
        logEncryption(encrypted_filename, key)
        return key


def decryptImage(filename: str, key: int):
    random.seed(key)
    with Image.open(filename) as image:
        pixels = image.load()

        for x in range(image.size[0]):
            for y in range(image.size[1]):
                pixel = pixels[x, y]
                pixels[x, y] = (
                    (pixel[0] - random.randint(0, 255)) % 256,
                    (pixel[1] - random.randint(0, 255)) % 256,
                    (pixel[2] - random.randint(0, 255)) % 256
                )

        decrypted_filename = addPostName(filename, "-d")
        image.save(decrypted_filename)


if __name__ == "__main__":
    while True:
        try:
            mode = input("<E>NCRYPT OR <D>ECRYPT (↵ to exit program) = ")
            print(HZNt)
            mode = mode.upper()

            if mode == 'E' or mode == 'ENCRYPT':
                filename = input("ENTER IMAGE NAME (WITH FULL PATH) = ")
                key = encryptImage(filename)
                print(HZNt)
                print(f"KEY = {key}")
                print(HZNt)

                while True:
                    delete_original = input("DO YOU WANT TO DELETE THE ORIGINAL? (Y/N) = ").lower()
                    print(HZNt)
                    if delete_original in ['y', 'yes']:
                        os.remove(filename)
                        print(HZNt)
                        print("DELETION SUCCESS")
                        print(HZNt)
                        break
                    elif delete_original in ['n', 'no']:
                        break

            elif mode == 'D' or mode == 'DECRYPT':
                filename = input("ENTER IMAGE NAME (WITH FULL PATH) = ")
                print(HZNt)
                key = int(input("KEY = "))
                decryptImage(filename, key)
                print(HZNt)
                print("DECRYPTION SUCCESS")
                print(HZNt)
            elif mode == '':
                exit(f'               ...BYE BYE...\n{HZNt}')
        except OSError as rte:
            print(HZNt)
            print('            >> TRY AGAIN ! <<')
            print(HZNt)
            print(rte)
            print(HZNt)

