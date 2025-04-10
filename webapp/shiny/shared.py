from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "WA_Fn-UseC_-Telco-Customer-Churn.csv")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

label_encoder = LabelEncoder()

df['Churn'] = label_encoder.fit_transform(df['Churn'])
