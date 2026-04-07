import pandas as pd

df = pd.read_csv("data/sample_data.csv")

# Convert date format
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Save back
df.to_csv("data/sample_data.csv", index=False)

print("Date format fixed")
print(df.head())