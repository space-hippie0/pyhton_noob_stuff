from PIL import Image
import random
import os

LOGFILE = "logfile.txt"
HZNt = 66 * '-'


def addPostName(filename, postfix):
    name, ext = os.path.splitext(filename)
    return f'{name}{postfix}{ext}'


def logEncryption(filename, key):
    with open(LOGFILE, "a") as log_file:
        log_file.write(f'{filename}, {key}\n')


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
    print(HZNt)
    while True:
        try:
            mode = input("<E>NCRYPT OR <D>ECRYPT      (↵ to exit program) = ")
            print(HZNt)
            mode = mode.upper()

            if mode == 'E' or mode == 'ENCRYPT':
                filename = input("ENTER IMAGE NAME (start with \'/\' for full path) = ")
                key = encryptImage(filename)
                print(f'{HZNt}KEY = {key}{HZNt}')

                while True:
                    delete_original = input("DO YOU WANT TO DELETE THE ORIGINAL? (Y/N) = ").upper()
                    print(HZNt)

                    if delete_original in ['Y', 'YES']:
                        os.remove(filename)
                        print(f'{HZNt}                     >> DELETION SUCCESS <<{HZNt}')
                        break
                    elif delete_original in ['N', 'NO']:
                        break

            elif mode == 'D' or mode == 'DECRYPT':
                filename = input("ENTER IMAGE NAME (start with \'/\' for full path) = ")
                print(HZNt)
                while True:
                    try:
                        key = int(input("KEY = "))
                        decryptImage(filename, key)
                        break
                    except ValueError as rte2:
                        print(f'{HZNt}\n!!! ERROR = {rte2} !!!\n{HZNt}')
                print(f'{HZNt}                     >> DECRYPTION SUCCESS <<{HZNt}')

            elif mode == '':
                exit(f'                        ... BYE BYE ...\n{HZNt}')
        except FileNotFoundError as rte:
            print(f'{HZNt}\n                         >> TRY AGAIN ! <<\n{2*HZNt}\n!!! ERROR = {rte} !!!\n{2*HZNt}')
