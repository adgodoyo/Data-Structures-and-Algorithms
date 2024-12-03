def change(money):
    # Crear una lista para almacenar el número mínimo de monedas para cada monto
    min_coins = [float('inf')] * (money + 1)
    min_coins[0] = 0  # Base: se necesitan 0 monedas para un total de 0

    # Monedas disponibles
    coins = [1, 3, 4]

    # Calcular el número mínimo de monedas para cada monto hasta "money"
    for m in range(1, money + 1):
        for coin in coins:
            if m >= coin:
                min_coins[m] = min(min_coins[m], min_coins[m - coin] + 1)

    return min_coins[money]


if __name__ == '__main__':
    m = int(input())
    print(change(m))
