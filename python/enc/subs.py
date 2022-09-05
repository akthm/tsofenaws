import random
key_name = ""
key = {}
inv_key = {}
key_saved = False
ALPHA = "abcdefghijklmnopqrstuvwxyz"


def set_key(seq):
    global key, inv_key
    for k in seq:
        inv_key[seq[k]] = k
    key = seq


def write_key(file):
    global key, key_saved, key_name
    file.write(key_name + "\n")
    line = ""
    for k in key:
        line += (k + "-" + key[k] + ",")
    file.write(line[:(len(line) - 1)])

    key_saved = True


def save_key(args):
    global key_name
    if not key:
        print("There is no key in memory!")
        return
    if len(args) != 1:
        print("usage : save <filename>")
        return
    try:
        f = open(args[0], 'w+')
        write_key(f)
        f.close()
        print(key_name, " saved in ", args[0])
    except OSError:
        print("saving key failed")


def read_key(file):
    global key, key_saved, key_name
    seq = {}
    name = file.readline()
    name = name.strip()
    line = file.readline()
    line = line.strip()
    blocks = line.split(",")
    for block in blocks:
        seq[block[0]] = block[2]
    key_name = name
    set_key(seq)
    key_saved = True


def load_key(args):
    global key, key_name
    if len(args) != 1:
        print("usage : load <filename>")
        return
    try:
        f = open(args[0], 'r')
        read_key(f)
        f.close()
        print(key_name, " loaded.", )
    except OSError:
        print("key file is not found")


def generate_sequence():
    seq = {}
    seq_len = random.randint(1, 13)
    legit_chars = [c for c in ALPHA]
    for i in range(seq_len):
        d_char = random.choice(legit_chars)
        legit_chars.remove(d_char)
        c_char = random.choice(legit_chars)
        legit_chars.remove(c_char)
        seq[d_char] = c_char
    return seq


def gen_key(args):
    global key, key_name, key_saved
    if len(args) != 1:
        print("usage : newkey <keyname>")
        return
    key_name = args[0]
    set_key(generate_sequence())
    key_saved = False
    print(key_name, "generated")


def print_info():
    print("current key: " + (key_name if key_name else "NO-KEY"))
    print("state: " + ("saved" if key_saved else "not saved"))
    print("Encryption:")
    print("\t" + ALPHA)
    line = ""
    for c in ALPHA:
        if c in key.keys():
            line += key[c]
        elif c in inv_key.keys():
            line += "."
        else:
            line += " "
    print("\t" + line)
    print("Decryption:")
    print("\t" + ALPHA)
    inv_line = ""
    for c in ALPHA:
        if c in key.keys():
            inv_line += "."
        elif c in inv_key.keys():
            inv_line += inv_key[c]
        else:
            inv_line += " "
    print("\t" + inv_line)


def encrypt_line(line):
    new_line = ""
    for c in line:
        if c in key:
            new_line += key[c]
        else:
            new_line += c
    return new_line


def decrypt_line(line):
    new_line = ""
    for c in line:
        if c in inv_key:
            new_line += inv_key[c]
        else:
            new_line += c
    return new_line


def cipher(args, func):
    if not key:
        print("there is no key")
        return
    if len(args) != 2:
        print("usage : enc/dec <source> <output>")
        return
    try:
        infile = open(args[0], "r")
        outfile = open(args[1], "w+")
        for line in infile:
            new_line = func(line)
            outfile.write(new_line)

        command = "Encryption" if func == encrypt_line else "Decryption"
        command += " is successful {" + args[0] + " -> " + args[1] + "}"
        print(command)
    except OSError:
        print("invalid file")


def parse_args(arg):
    command = arg[0]
    if command == 'save':
        save_key(arg[1:])
    elif command == 'load':
        load_key(arg[1:])
    elif command == 'newkey':
        gen_key(arg[1:])
    elif command == 'dec':
        cipher(arg[1:], decrypt_line)
    elif command == 'enc':
        cipher(arg[1:], encrypt_line)
    elif command == 'info':
        print_info()
    elif command == 'exit':
        exit()
    else:
        print("invalid command! (choose from 'save', 'load', 'dec', 'enc', 'info', 'newkey', 'exit')")


def shell():
    while True:
        arg = input("sub>")
        parse_args(arg.split())


if __name__ == '__main__':
    shell()

