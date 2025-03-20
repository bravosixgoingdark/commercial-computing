import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy.stats import chi2_contingency

# Load Dataset
file_path = './WA_Fn-UseC_-Telco-Customer-Churn.csv'
df = pd.read_csv(file_path)

# Display basic info
print(df.info())
print(df.head())

# Convert 'TotalCharges' to numeric, handling errors
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Fill missing values
df.fillna({'TotalCharges': df['TotalCharges'].median()}, inplace=True)

# Drop 'customerID' as it's not useful for analysis
df.drop(columns=['customerID'], inplace=True)

# Encode categorical variables
label_encoders = {}
categorical_columns = df.select_dtypes(include=['object']).columns
df_encoded = df.copy()

for col in categorical_columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Scale numerical features
scaler = StandardScaler()
numerical_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']
df_encoded[numerical_columns] = scaler.fit_transform(df_encoded[numerical_columns])

# Data Visualization
visualization = plt.figure(figsize=(12,6))
visualization = sns.countplot(x='Churn', data=df, palette='coolwarm')
plt.title('Customer Churn Distribution')
plt.xlabel('Churn')
plt.ylabel('Count')
plt.show()

# Churn rate by contract type
churnrate = plt.figure(figsize=(12,6))
churnrate = sns.countplot(x='Contract', hue='Churn', data=df, palette='coolwarm')
plt.title('Churn Rate by Contract Type')
plt.xlabel('Contract Type')
plt.ylabel('Count')
plt.show()

# Monthly Charges distribution by churn status
charges_distribution = plt.figure(figsize=(12,6))
charges_distribution = sns.histplot(df, x='MonthlyCharges', hue='Churn', kde=True, palette='coolwarm')
plt.title('Monthly Charges Distribution by Churn Status')
plt.xlabel('Monthly Charges')
plt.ylabel('Density')
plt.show()

# Tenure distribution by churn status
tenure_distribution = plt.figure(figsize=(12,6))
tenure_distribution = sns.histplot(df, x='tenure', hue='Churn', kde=True, palette='coolwarm')
plt.title('Tenure Distribution by Churn Status')
plt.xlabel('Tenure (Months)')
plt.ylabel('Density')
plt.show()

# Statistical Analysis - Chi-Square Test
contingency_table = pd.crosstab(df['Contract'], df['Churn'])
chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-Square Test P-Value (Contract vs Churn): {p}")

contingency_table2 = pd.crosstab(df['PaymentMethod'], df['Churn'])
chi2, p, dof, expected = chi2_contingency(contingency_table2)
print(f"Chi-Square Test P-Value (PaymentMethod vs Churn): {p}")

print("Data processing complete. Statistical analysis and visualization generated.")
