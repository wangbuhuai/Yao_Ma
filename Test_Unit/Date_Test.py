# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-15

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-15


from datetime import date


def main():
    d1 = date(2017, 2, 24)
    d2 = date(2022, 4, 28)
    num_of_days = d2 - d1
    print(num_of_days.days)


if __name__ == "__main__":
    main()
