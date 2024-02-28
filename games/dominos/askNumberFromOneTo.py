#!/usr/bin/env python3


def askNumberFromOneTo(inMax):
    intMax = int(inMax)
    if intMax < 1:
        return 1
    # print('inMax:', inMax, 'intMax:', intMax)
    print(f"Enter a number from 1 to {inMax}: ")
    s = input(f"Enter a number from 1 to {intMax}: ").lower()
    assert s[0] != "q"
    if s[0] == "u":
        return s[0]
    try:
        i = int(float(s))
    except (TypeError, ValueError):
        i = 0
    print("s:", s, "i:", i)
    return i if 1 <= i <= intMax else askNumberFromOneTo(intMax)


def main():
    print(f"Got: {askNumberFromOneTo(10.34)}")


if __name__ == "__main__":
    main()
