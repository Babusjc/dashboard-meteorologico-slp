
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_and_predict_weather(file_path="data/inmet_data_sao_luiz_do_paraitinga_combined.csv"):
    """Performs data analysis and builds a simple prediction model."""
    if not os.path.exists(file_path):
        print(f"Error: Data file not found at {file_path}")
        return

    df = pd.read_csv(file_path)

    print("\n--- Data Overview ---")
    print(df.head())
    print("\n--- Data Info ---")
    df.info()
    print("\n--- Basic Statistics ---")
    print(df.describe())

    # Convert 'DATA' to datetime objects
    df["DATA"] = pd.to_datetime(df["DATA"])
    df["MES"] = df["DATA"].dt.month
    df["DIA_DO_ANO"] = df["DATA"].dt.dayofyear

    # --- Machine Learning Model (Simple Linear Regression) ---
    # Predict average temperature based on month and day of year
    features = ["MES", "DIA_DO_ANO"]
    target = "TEMPERATURA_MEDIA"

    # Drop rows with NaN values in features or target
    df_ml = df.dropna(subset=features + [target])

    if df_ml.empty:
        print("Not enough data after dropping NaNs for ML model.")
        return

    X = df_ml[features]
    y = df_ml[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n--- Machine Learning Model Results ---")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R-squared (R2): {r2:.2f}")

    # --- Data Visualization (Example) ---
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=\

        "DATA", y="TEMPERATURA_MEDIA", data=df, label="Temperatura Média Real")
    plt.title("Temperatura Média ao Longo do Tempo em São Luiz do Paraitinga")
    plt.xlabel("Data")
    plt.ylabel("Temperatura Média (°C)")
    plt.grid(True)
    plt.savefig("data/temperatura_media_slp.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=y_pred)
    plt.xlabel("Temperatura Média Real (°C)")
    plt.ylabel("Temperatura Média Prevista (°C)")
    plt.title("Previsão vs. Real (Temperatura Média)")
    plt.grid(True)
    plt.savefig("data/previsao_vs_real_slp.png")
    plt.close()

    print("\n--- Visualizations Saved ---")
    print("temperatura_media_slp.png")
    print("previsao_vs_real_slp.png")

if __name__ == "__main__":
    analyze_and_predict_weather()


