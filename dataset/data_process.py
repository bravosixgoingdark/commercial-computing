
# Data process 2.0 - More accurate revised version
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
import numpy as np

df = pd.read_csv('./WA_Fn-UseC_-Telco-Customer-Churn.csv')

print(df.head())  # First, df.head() can be used to get an overview of the data
print(df.shape)  # Check the number of features and the number of data points in each feature
print(df.isnull().sum())  # No missing values

# customerID          0
# gender              0
# SeniorCitizen       0
# Partner             0
# Dependents          0
# tenure              0
# PhoneService        0
# MultipleLines       0
# InternetService     0
# OnlineSecurity      0
# OnlineBackup        0
# DeviceProtection    0
# TechSupport         0
# StreamingTV         0
# StreamingMovies     0
# Contract            0
# PaperlessBilling    0
# PaymentMethod       0
# MonthlyCharges      0
# TotalCharges        0
# Churn               0

print((df == " ").sum())  # Check the number of blank values in each column. 11 blank values in TotalCharges.
# customerID           0
# gender               0
# SeniorCitizen        0
# Partner              0
# Dependents           0
# tenure               0
# PhoneService         0
# MultipleLines        0
# InternetService      0
# OnlineSecurity       0
# OnlineBackup         0
# DeviceProtection     0
# TechSupport         0
# StreamingTV         0
# StreamingMovies      0
# Contract             0
# PaperlessBilling     0
# PaymentMethod       0
# MonthlyCharges       0
# TotalCharges        11
# Churn                0
# dtype: int64

# Drop unnecessary columns
df = df.drop(columns=["customerID"])

df["gender"] = df["gender"].replace({"Male": 1, "Female": 0})  # Optimized for RandomForest

# Handling missing values in TotalCharges: (7043, 21) dropping rows is more optimal than keeping them
df["TotalCharges"] = df["TotalCharges"].replace(" ", np.nan)  # Some missing values are stored as empty strings, replace them with NaN so Pandas recognizes them as missing values.
df = df.dropna(subset=["TotalCharges"])  # dropna will remove rows containing missing values

# Convert Yes/No categorical features into binary format for the model
binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling", "Churn"]

df[binary_cols] = df[binary_cols].replace({"Yes": 1, "No": 0})

# One-hot encoding for categorical features with no order
one_hot_cols = ["MultipleLines", "InternetService", "OnlineSecurity",
                "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
                "StreamingMovies", "PaymentMethod"]  # Fewer columns work well and do not significantly affect the final result, but this can be adjusted for better accuracy

df = pd.get_dummies(df, columns=one_hot_cols, drop_first=True)

# 0.9972980659840728 test 1 without normalization
# 0.9972980659840728 test 2 with normalization
# => No difference

# Ordinal Encoding for Contract (which has an order)
contract_encoder = OrdinalEncoder(categories=[["Month-to-month", "One year", "Two year"]])
df["Contract"] = contract_encoder.fit_transform(df[["Contract"]])  # Best approach

X = df.drop(columns=["Churn"])
y = df["Churn"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

feature_importance_df = pd.DataFrame({
    "Feature": df.drop(columns=["Churn"]).columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x="Importance", y="Feature", data=feature_importance_df.head(21), palette="viridis")
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Top 21 Most Important Features")
plt.show()

accuracy = model.score(X, y)
print("Accuracy:.....................................................", accuracy)  # 0.9972980659840728 nearly perfect => Data can be used

