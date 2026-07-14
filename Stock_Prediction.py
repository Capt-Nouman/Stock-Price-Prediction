import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

print("=" * 60)
print("STOCK PRICE PREDICTION USING MACHINE LEARNING")
print("=" * 60)

# Stock Symbol
stock_symbol = "AAPL"

print(f"\nDownloading {stock_symbol} stock data...")

# Download historical stock data
data = yf.download(
    stock_symbol,
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# Create target column (next day's closing price)
data["Next_Close"] = data["Close"].shift(-1)

# Remove missing values
data.dropna(inplace=True)

# Features and Target
X = data[["Open", "High", "Low", "Volume"]]
y = data["Next_Close"]

# Train-Test Split (Time Series Style)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

print("\nTraining Random Forest Model...")

# Random Forest Regressor
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

print("Generating Predictions...")

# Predictions
predictions = model.predict(X_test)

# Evaluation Metrics
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("-" * 30)
print(f"Mean Absolute Error : {mae:.2f}")
print(f"R² Score            : {r2:.4f}")

# Results DataFrame
results = pd.DataFrame({
    "Date": y_test.index,
    "Actual Price": y_test.values,
    "Predicted Price": predictions
})

print("\nSample Predictions")
print(results.head(10))

# Save predictions to CSV
results.to_csv("Predicted_Stock_Prices.csv", index=False)

print("\nPrediction file saved successfully!")
print("File Name: Predicted_Stock_Prices.csv")

# Plot Actual vs Predicted Prices
plt.figure(figsize=(12, 6))

plt.plot(
    y_test.values,
    label="Actual Price"
)

plt.plot(
    predictions,
    label="Predicted Price"
)

plt.title(f"{stock_symbol} Stock Price Prediction")
plt.xlabel("Days")
plt.ylabel("Closing Price")
plt.legend()

plt.tight_layout()
plt.show()

print("\nProject Completed Successfully!")
