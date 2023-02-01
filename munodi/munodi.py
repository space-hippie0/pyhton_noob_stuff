# easy file ==> PATH = 'text_simple.txt'
PATH = 'text_long.txt'
list_of_seqs = []


def reader(path_):
    try:
        with open(path_, 'r', encoding='utf-8') as infile:

            for line in infile.readlines():
                list_of_seqs.append([int(x) for x in line.rstrip().split()])

    except OSError as rte:
        exit(f"sorry mate {rte}")

    return list_of_seqs


def checker(list_):
    try:

        for seq in list_:
            length_ = len(seq)

            for m in range(length_ - 1):
                if seq[m] % 2 == 0:
                    if seq[m+1] != seq[m]/2:
                        print(f"Sorry mate, not a munodi sequence.   :(")
                        break

                if seq[m] % 2 == 1:
                    if seq[m+1] != 3*seq[m] + 1:
                        print(f"Sorry mate, not a munodi sequence.   :(")
                        break
            else:
                print(f"Congrats, it is a munodi sequence! >>{length_}<<")

    except OSError as rte:
        exit(f"well something went wrong for sure ==> {rte}")


def main():
    checker(reader(PATH))


if __name__ == '__main__':
    main()
