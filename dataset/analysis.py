
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data.dropna(inplace=True)

label_encoder = LabelEncoder()
data['Churn'] = label_encoder.fit_transform(data['Churn'])  # Yes=1, No=0

gender_table = data.groupby(['gender', 'Churn']).size().unstack().fillna(0)
gender_table.columns = ['Not Churned', 'Churned']
gender_table.to_csv('gender_table.csv')

plt.figure(figsize=(8, 6))
sns.barplot(x='Contract', y='Churn', data=data)
plt.title('Churn Rate by Contract Type')
plt.xlabel('Contract Type')
plt.ylabel('Churn Rate')
plt.savefig('churn_rate_contract.png')
plt.close()

plt.figure(figsize=(8, 6))
sns.barplot(x='InternetService', y='Churn', data=data)
plt.title('Churn Rate by Internet Service Type')
plt.xlabel('Internet Service Type')
plt.ylabel('Churn Rate')
plt.savefig('churn_rate_internet_service.png')
plt.close()

plt.figure(figsize=(10, 6))
sns.countplot(y='PaymentMethod', hue='Churn', data=data)
plt.title('Churn Distribution by Payment Method')
plt.xlabel('Number of Customers')
plt.ylabel('Payment Method')
plt.savefig('churn_distribution_payment_method.png')
plt.close()

plt.figure(figsize=(8, 6))
sns.boxplot(x='Churn', y='MonthlyCharges', data=data)
plt.title('Monthly Charges Distribution by Churn Status')
plt.xlabel('Churn Status')
plt.ylabel('Monthly Charges')
plt.savefig('monthly_charges_distribution.png')
plt.close()

plt.figure(figsize=(8, 6))
sns.histplot(data=data, x='tenure', hue='Churn', multiple='stack', bins=30)
plt.title('Tenure Distribution by Churn Status')
plt.xlabel('Tenure (Months)')
plt.ylabel('Number of Customers')
plt.savefig('tenure_distribution_churn.png')
plt.close()

print(" Visualizations and gender summary exported successfully for Shiny dashboard.")
