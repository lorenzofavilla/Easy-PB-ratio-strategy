import pandas as pd

def calculate_weights(sheet_index):
    df_original = pd.read_excel("MONTHLY.xlsx", sheet_name=sheet_index)
    df_original = df_original.dropna()
    pb_column = df_original.columns[1]
    df_sorted = df_original.sort_values(by=pb_column)  # sort values by PB ratio
    pb_ratios = df_sorted.iloc[:, 1]  # PB ratio column
    decile_length = int(pb_ratios.shape[0] / 10)
    market_value = df_sorted.iloc[:, 2]  # market value (MKT CAP) column

    first_decile_mv = market_value.iloc[:decile_length]
    tenth_decile_mv = market_value.iloc[-decile_length:]

    total_mv_first_decile = first_decile_mv.sum()
    total_mv_tenth_decile = tenth_decile_mv.sum()

    weight_first_decile = [mv / total_mv_first_decile for mv in first_decile_mv]
    weight_tenth_decile = [mv / total_mv_tenth_decile for mv in tenth_decile_mv]

    price_first_decile = list(df_sorted.iloc[:decile_length, 4])
    price_tenth_decile = list(df_sorted.iloc[-decile_length:, 4])

    return weight_first_decile, weight_tenth_decile, price_first_decile, price_tenth_decile, decile_length

def calculate_profit_loss(results, start_month, end_month):
    decile_length_start = results[f'decile_length_{start_month}']
    weights_first_start = results[f'weights_first_decile_{start_month}']
    prices_first_start = results[f'prices_first_decile_{start_month}']
    weights_first_end = results[f'weights_first_decile_{end_month}']
    prices_first_end = results[f'prices_first_decile_{end_month}']
    weights_tenth_start = results[f'weights_tenth_decile_{start_month}']
    prices_tenth_start = results[f'prices_tenth_decile_{start_month}']
    weights_tenth_end = results[f'weights_tenth_decile_{end_month}']
    prices_tenth_end = results[f'prices_tenth_decile_{end_month}']
    
    profit_loss = []
    for i in range(decile_length_start):
        pl = (weights_first_end[i] * prices_first_end[i] - weights_first_start[i] * prices_first_start[i]) + \
             (weights_tenth_start[i] * prices_tenth_start[i] - weights_tenth_end[i] * prices_tenth_end[i])
        profit_loss.append(pl)
    
    profit_loss_df = pd.DataFrame(profit_loss)
    return profit_loss_df.sum().values[0]  # Ensure it is a scalar

# Define months from July 2023 to May 2024
months = ["07_2023", "08_2023", "09_2023", "10_2023", "11_2023", "12_2023", 
          "01_2024", "02_2024", "03_2024", "04_2024", "05_2024"]
results = {}

# Populate the results dictionary
for i, month in enumerate(months):
    weights_first_decile, weights_tenth_decile, prices_first_decile, prices_tenth_decile, decile_length = calculate_weights(i)
    results[f'weights_first_decile_{month}'] = weights_first_decile
    results[f'weights_tenth_decile_{month}'] = weights_tenth_decile
    results[f'prices_first_decile_{month}'] = prices_first_decile
    results[f'prices_tenth_decile_{month}'] = prices_tenth_decile
    results[f'decile_length_{month}'] = decile_length

# Calculate investment for July 2023
investment = [results['weights_first_decile_07_2023'][i] * results['prices_first_decile_07_2023'][i] for i in range(results['decile_length_07_2023'])]
investment_df = pd.DataFrame(investment)
total_investment = investment_df.sum().values[0]  # Ensure it is a scalar
print("Total Investment in July 2023: ", total_investment)

# Calculate total profit loss over all periods
total_profit_loss = 0
for start_month in months[:-1]:
    end_month = months[months.index(start_month) + 1]
    total_profit_loss += calculate_profit_loss(results, start_month, end_month)
    total_return = total_profit_loss / total_investment * 100
    print(f"Total return as of month {end_month}: {total_return:.2f}%")

