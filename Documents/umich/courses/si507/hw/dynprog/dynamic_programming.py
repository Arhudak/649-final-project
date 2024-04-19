import math

def change(amount, coins):
    # Create a table to store the minimum number of coins required
    dp = [math.inf] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make 0 amount
    
    # Iterate through each coin denomination
    for coin in coins:
        # Update the table values for each possible amount
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # If the value at the target amount is still infinity, return math.inf
    if dp[amount] == math.inf:
        return math.inf
    else:
        return dp[amount]

def giveChange(amount, coins):
    dp = [math.inf] * (amount + 1)
    dp[0] = 0
    
    # Store the selected coins for each amount
    selected_coins = [[] for _ in range(amount + 1)]
    
    for coin in coins:
        for i in range(coin, amount + 1):
            if dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                # Update the selected coins list
                selected_coins[i] = selected_coins[i - coin] + [coin]
    
    if dp[amount] == math.inf:
        return [math.inf, []]
    else:
        return [dp[amount], selected_coins[amount]]

def main():
    # Test cases
    test_cases = [
        (48, [1, 5, 10, 25, 50]),
        (48, [1, 7, 24, 42]),
        (35, [1, 3, 16, 30, 50]),
        (6, [4, 5, 9])
    ]
    
    for amount, coins in test_cases:
        print(f"Amount: {amount}, Coins: {coins}")
        print("Minimum number of coins:", change(amount, coins))
        print("List of coins:", giveChange(amount, coins))
        print()


if __name__ == "__main__":
	main()