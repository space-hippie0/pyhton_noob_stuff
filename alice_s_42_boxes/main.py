#FILENAME = 'input_files/actions-simple.txt'
#FILENAME = 'input_files/actions-fail_carl.txt'
#FILENAME = 'input_files/actions-fail_bob.txt'
FILENAME = 'input_files/actions.txt'


magic_boxes = [[] for i in range(42)]


def find_box(boxes, fruit):
    for index, box in enumerate(boxes):
        if fruit in box:
            return index
    for index, box in enumerate(boxes):
        if not box:
            return index
    return None


def add_object(boxes, fruit):
    bi = find_box(boxes, fruit)
    if bi is None:
        return False
    else:
        boxes[bi].append(fruit)
        return True


def remove_object(boxes, fruit):
    bi = find_box(boxes, fruit)
    if bi is None or not boxes[bi]:
        return False
    else:
        boxes[bi].pop()
        return True


def main():
    try:
        with open(FILENAME) as infile:
            for actions in infile:
                actor, action, a, fruit = actions.split()
                if actor.upper() == 'BOB':
                    if not add_object(magic_boxes, fruit):
                        quit(f"Alice cannot store a {fruit} given by {actor}!")

                elif actor.upper() == 'CARL':
                    if not remove_object(magic_boxes, fruit):
                        quit(f"Alice cannot give {actor} a {fruit}!")
                else:
                    quit('unknown actor')
        print(4*'=>', 'Yeah... ok', 4*'<=')

    except OSError as err:
        quit(f'sorry mate that\'s an {err}')

    mgbx = input("you wanna see the boxes? (Y/N)   #")
    if mgbx.upper() == 'Y':
        print(magic_boxes)
    elif mgbx.upper() == 'N':
        exit("ok")
    else:
        exit("that's fine too")


if __name__ == '__main__':
    main()
