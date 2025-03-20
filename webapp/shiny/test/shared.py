from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "WA_Fn-UseC_-Telco-Customer-Churn.csv")

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

df.fillna({'TotalCharges': df['TotalCharges'].median()}, inplace=True)

df.drop(columns=['customerID'], inplace=True)

label_encoders = {}
categorical_columns = df.select_dtypes(include=['object']).columns
df_encoded = df.copy()
for col in categorical_columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le

scaler = StandardScaler()
numerical_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']
df_encoded[numerical_columns] = scaler.fit_transform(df_encoded[numerical_columns])

