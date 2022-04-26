# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-19

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-19


import re
from re import search


def main():
    text1 = "NUSTAR GP HOLDINGS L L C"
    text2 = "abcd-x.'y  z"
    print(search(r"\bL\W*?L\W*?C\W*$|\bCORP\W*$|\bCO\W*$|\bL\W*?T\W*?D\W*$", text1, re.IGNORECASE))


if __name__ == "__main__":
    main()
