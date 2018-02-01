from FiatShamir import FiatShamir


def main():
    fs1 = FiatShamir(index=105)
    print(fs1.new_user("U1", 13))
    print(fs1.new_user("U2", 12))
    print(fs1.new_user("U3", 10))

    fs2 = FiatShamir()
    print(fs2.new_user("U4", 14))
    print(fs2.new_user("U5", 15))

    print(fs1.new_user("U6", 16))


if __name__ == "__main__":
    main()
