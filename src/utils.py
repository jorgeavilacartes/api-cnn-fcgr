def clean_seq(seq):
    "Remove all characters different from A,C,G,T or N"
    seq = seq.upper()
    for letter in "BDEFHIJKLMOPQRSUVWXYZ":
        seq = seq.replace(letter,"N")
    return seq