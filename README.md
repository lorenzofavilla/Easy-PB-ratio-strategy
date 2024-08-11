Hi there!

Welcome to my project on decile-based trading strategies using monthly data for the Topix index, which includes around 2100 stocks. This project was developed in my free time to explore simple trading strategies based on Price-to-Book (PB) ratios.

Project Overview:
  **Monthly Data Analysis**: The analysis covers a period from July 2023 to May 2024, using monthly data.
  **Data Preprocessing**: The dataset, sourced from Reuters, includes PB ratios and market values for Topix index stocks. Rows with missing data are removed to ensure accurate analysis.
  **Decile Calculation**: Stocks are sorted by their PB ratios and divided into deciles. The top decile (first decile) and bottom decile (tenth decile) are used to compute market value weights.
  **Long-Short Strategy**: A long-short strategy is evaluated by going long on the top decile and short on the bottom decile.
  **Profit/Loss Calculation**: The strategy’s performance is calculated by analyzing the changes in decile weights and prices over time. The results are accumulated to provide insights into the strategy’s effectiveness.
