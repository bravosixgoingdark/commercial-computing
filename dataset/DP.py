# Complete Telecom Customer Churn Prediction Pipeline (Full Script with Preprocessing, Modeling, and Visualizations)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# --------------------------------------------------------------------------------------------
# Step 1: Load Dataset and Initial Preprocessing
# --------------------------------------------------------------------------------------------
data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Convert TotalCharges to numeric and drop missing values
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data.dropna(subset=['TotalCharges'], inplace=True)
data.drop('customerID', axis=1, inplace=True)

# Encode categorical features
categorical_cols = data.select_dtypes(include=['object']).columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Replace encoded Churn back to Yes/No for visualization
data['Churn'] = data['Churn'].map({0: 'No', 1: 'Yes'})

# Preserve original (unscaled) columns for visualization
viz_data = data.copy()

# Feature scaling
scaler = StandardScaler()
numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

# --------------------------------------------------------------------------------------------
# Step 2: Split Data and Train Model
# --------------------------------------------------------------------------------------------
X = data.drop('Churn', axis=1)
y = data['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

model = RandomForestClassifier(n_estimators=300, max_depth=12, min_samples_split=10,
                               min_samples_leaf=4, random_state=42)
model.fit(X_train, y_train)

# --------------------------------------------------------------------------------------------
# Step 3: Evaluate Model
# --------------------------------------------------------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2%}")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

# --------------------------------------------------------------------------------------------
# Step 4: Feature Importance Visualization
# --------------------------------------------------------------------------------------------
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df.head(15), hue='Feature', dodge=False, legend=False, palette='viridis')
plt.title('Top 15 Feature Importances in Predicting Churn')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.tight_layout(rect=[0, 0, 0.95, 1])
plt.savefig('feature_importance.png')
plt.show()

# --------------------------------------------------------------------------------------------
# Step 5: Visualizations for EDA (Improved)
# --------------------------------------------------------------------------------------------

# 1. Churn Distribution with Percentages
plt.figure(figsize=(6, 4))
churn_counts = data['Churn'].value_counts(normalize=True) * 100
sns.barplot(x=churn_counts.index, y=churn_counts.values, hue=churn_counts.index, legend=False, palette='Set2', showlegend=False)
plt.title('Churn Distribution (%)')
plt.xlabel('Churn')
plt.ylabel('Percentage')
for i, val in enumerate(churn_counts.values):
    plt.text(i, val + 1, f"{val:.1f}%%", ha='center', fontsize=12)
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig('churn_distribution_percent.png')
plt.show()

# 2. Monthly Charges vs Churn (Stacked Column Chart)

# Bin Monthly Charges
viz_data['MonthlyCharges_Bin'] = pd.cut(viz_data['MonthlyCharges'], bins=[0, 20, 40, 60, 80, 100, 120, np.inf])
monthly_churn_grouped = viz_data.groupby(['MonthlyCharges_Bin', 'Churn'], observed=False).size().unstack(fill_value=0)

# Plot stacked column chart with Churn counts and label 'Yes' churn count
ax = monthly_churn_grouped.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#d0d1e6', '#de2d26'])
plt.title('Customer Churn Count by Monthly Charges Range')
plt.xlabel('Monthly Charges Range')
plt.ylabel('Customer Count')
plt.xticks(rotation=45)
plt.legend(title='Churn')

# Annotate each bar segment with 'Yes' churn count
for index, row in monthly_churn_grouped.iterrows():
    total = row.sum()
    yes_churn = row.get('Yes', 0)
    percent = (yes_churn / total) * 100 if total > 0 else 0
    x_pos = list(monthly_churn_grouped.index).index(index)
    ax.text(x=x_pos, y=total + 5, s=f"{yes_churn} ({percent:.1f}%)", ha='center', fontsize=10, color='black', fontweight='bold')

plt.tight_layout()
plt.savefig('monthlycharges_stacked_churn_updated.png')
plt.show()


# 4. Internet Service Type vs. Churn (All Service Types, Stacked Column Chart with Percentage Labels)

# Map encoded InternetService values back to readable labels
viz_data['InternetService'] = pd.Series(label_encoders['InternetService'].inverse_transform(viz_data['InternetService']), index=viz_data.index)

# Group and calculate churn percentages
internet_grouped = viz_data.groupby(['InternetService', 'Churn']).size().unstack(fill_value=0)
internet_grouped['Total'] = internet_grouped.sum(axis=1)
internet_grouped['Churn %'] = (internet_grouped['Yes'] / internet_grouped['Total']) * 100
internet_grouped = internet_grouped.drop(columns='Total')

# Plot stacked column chart

ax3 = internet_grouped.drop(columns='Churn %').plot(kind='bar', stacked=True, figsize=(10, 6), color=['#d0d1e6', '#de2d26'])
plt.title('Customer Churn by Internet Service Type')
plt.xlabel('Internet Service Type')
plt.ylabel('Customer Count')
plt.xticks(rotation=0)
plt.legend(title='Churn')

for i, (label, row) in enumerate(internet_grouped.iterrows()):
    yes = row['Yes']
    pct = row['Churn %']
    total = row['Yes'] + row['No']
    ax3.text(i, total + 5, f"{int(yes)} ({pct:.1f}%)", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

plt.savefig('internetservice_churn_stacked_column.png')
plt.show()

# 3. Tenure vs. Churn Count by Bins (Y-axis = Tenure bins, X-axis = Churn Count)

# Define custom bins for Tenure to improve clarity
tenure_bins = [0, 12, 24, 36, 48, 60, 72]
viz_data['Tenure_Bin'] = pd.cut(viz_data['tenure'], bins=tenure_bins)
tenure_churn_grouped = viz_data.groupby(['Tenure_Bin', 'Churn'], observed=False).size().unstack(fill_value=0)

# Plot stacked bar chart with labels for 'Yes' churn
ax2 = tenure_churn_grouped.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#c6dbef', '#ef3b2c'])
plt.title('Customer Churn Count by Tenure Range')
plt.xlabel('Tenure Range (Months)')
plt.ylabel('Customer Count')
plt.xticks(rotation=45)
plt.legend(title='Churn')

# Add annotation for churned customers
for i, row in enumerate(tenure_churn_grouped.itertuples()):
    total = getattr(row, 'No', 0) + getattr(row, 'Yes', 0)
    yes = getattr(row, 'Yes', 0)
    pct = (yes / total) * 100 if total > 0 else 0
    ax2.text(i, total + 5, f"{int(yes)} ({pct:.1f}%)", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

plt.tight_layout()
plt.savefig('tenure_churn_stacked_column.png')
plt.show()



# --------------------------------------------------------------------------------------------
# 6. Contract Type vs. Churn (Stacked Column with Percentages)

# Map Contract back to labels
viz_data['Contract'] = pd.Series(label_encoders['Contract'].inverse_transform(viz_data['Contract']), index=viz_data.index)
contract_grouped = viz_data.groupby(['Contract', 'Churn']).size().unstack(fill_value=0)
contract_grouped['Total'] = contract_grouped.sum(axis=1)
contract_grouped['Churn %'] = (contract_grouped['Yes'] / contract_grouped['Total']) * 100
contract_grouped = contract_grouped.drop(columns='Total')

ax4 = contract_grouped.drop(columns='Churn %').plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Accent')
plt.title('Customer Churn by Contract Type')
plt.xlabel('Contract Type')
plt.ylabel('Customer Count')
plt.xticks(rotation=0)
plt.legend(title='Churn')

for i, (label, row) in enumerate(contract_grouped.iterrows()):
    yes = row['Yes']
    pct = row['Churn %']
    total = row['Yes'] + row['No']
    ax4.text(i, total + 5, f"{int(yes)} ({pct:.1f}%)", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

plt.tight_layout()
plt.savefig('contract_churn_stacked_column.png')
plt.show()

# 7. OnlineSecurity vs. Churn (Stacked Column with Percentages)

viz_data['OnlineSecurity'] = pd.Series(label_encoders['OnlineSecurity'].inverse_transform(viz_data['OnlineSecurity']), index=viz_data.index)
onlinesec_grouped = viz_data.groupby(['OnlineSecurity', 'Churn']).size().unstack(fill_value=0)
onlinesec_grouped['Total'] = onlinesec_grouped.sum(axis=1)
onlinesec_grouped['Churn %'] = (onlinesec_grouped['Yes'] / onlinesec_grouped['Total']) * 100
onlinesec_grouped = onlinesec_grouped.drop(columns='Total')

ax5 = onlinesec_grouped.drop(columns='Churn %').plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Paired')
plt.title('Customer Churn by Online Security Status')
plt.xlabel('Online Security')
plt.ylabel('Customer Count')
plt.xticks(rotation=0)
plt.legend(title='Churn')

for i, (label, row) in enumerate(onlinesec_grouped.iterrows()):
    yes = row['Yes']
    pct = row['Churn %']
    total = row['Yes'] + row['No']
    ax5.text(i, total + 5, f"{int(yes)} ({pct:.1f}%)", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

plt.tight_layout()
plt.savefig('onlinesecurity_churn_stacked_column.png')
plt.show()

# --------------------------------------------------------------------------------------------
# Final Note:
# --------------------------------------------------------------------------------------------
# Visuals updated with churn percentages for deeper business insights.
