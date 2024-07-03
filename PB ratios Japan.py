import pandas as pd

def calculate_weights(sheet_index):
    df_original = pd.read_excel("PB ratios Japan.xlsx", sheet_name=sheet_index)
    pb_column = df_original.columns[1]
    df_sorted = df_original.sort_values(by=pb_column) # sort values by PB
    pb_ratios = df_sorted.iloc[:, 1] # PB ratio column
    decile_length = int(pb_ratios.shape[0] / 10)
    market_value = df_sorted.iloc[:, 2] # market value (MKT CAP) column

    first_decile_mv = market_value.iloc[:decile_length]
    tenth_decile_mv = market_value.iloc[-decile_length:]

    total_mv_first_decile = first_decile_mv.sum()
    total_mv_tenth_decile = tenth_decile_mv.sum()

    weight_first_decile = [mv / total_mv_first_decile for mv in first_decile_mv]
    weight_tenth_decile = [mv / total_mv_tenth_decile for mv in tenth_decile_mv]

    price_first_decile = list(df_sorted.iloc[:decile_length, 4].dropna())
    price_tenth_decile = list(df_sorted.iloc[-decile_length:, 4].dropna())

    return weight_first_decile, weight_tenth_decile, price_first_decile, price_tenth_decile, decile_length

weights_first_decile_2022, weights_tenth_decile_2022, prices_first_decile_2022, prices_tenth_decile_2022, decile_length = calculate_weights(0)
weights_first_decile_2024, weights_tenth_decile_2024, prices_first_decile_2024, prices_tenth_decile_2024, decile_length = calculate_weights(1)

# Long-short strategy: long 1st decile, short 10th decile
profit_loss = []
for i in range(decile_length):
    pl = (weights_first_decile_2024[i] * prices_first_decile_2024[i] - weights_first_decile_2022[i] * prices_first_decile_2022[i]) - \
         (weights_tenth_decile_2022[i] * prices_tenth_decile_2022[i] - weights_tenth_decile_2024[i] * prices_tenth_decile_2024[i])
    profit_loss.append(pl)

profit_loss_df = pd.DataFrame(profit_loss)
total_profit_loss = profit_loss_df.sum().values[0]  # Ensure it is a scalar

# In 2022, the long investment would have cost total_investment
investment = [weights_first_decile_2022[i] * prices_first_decile_2022[i] for i in range(decile_length)]
investment_df = pd.DataFrame(investment)
total_investment = investment_df.sum().values[0]  # Ensure it is a scalar

# Total return (not considering shorting fees)
total_return = total_profit_loss / total_investment * 100

print(f"Total return: {total_return:.2f}%")
