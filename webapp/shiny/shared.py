from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "WA_Fn-UseC_-Telco-Customer-Churn.csv")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

label_encoder = LabelEncoder()
df['Churn'] = label_encoder.fit_transform(df['Churn'])

df['Churn'] = df['Churn'].map({0: 'No', 1: 'Yes'})

# Additional preprocessing for DP.py charts
df['MonthlyCharges_Bin'] = pd.cut(df['MonthlyCharges'], bins=[0, 20, 40, 60, 80, 100, 120, float('inf')], labels=['0-20', '21-40', '41-60', '61-80', '81-100', '101-120', '120+'])
df['Tenure_Bin'] = pd.cut(df['tenure'], bins=[0, 12, 24, 36, 48, 60, 72], labels=['0-12', '13-24', '25-36', '37-48', '49-60', '61-72'])
