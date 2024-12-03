def change(money):
    coins = 0

    coins += money // 10
    money %= 10

    coins += money // 5
    money %= 5

    coins += money

    return coins

if __name__ == '__main__':
    m = int(input())
    print(change(m))
