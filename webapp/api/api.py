# churn_model_backend.py — Single Best Model Only (Gradient Boosting Classifier)

import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from flask import Flask, jsonify, request

app = Flask(__name__)

data = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data.dropna(inplace=True)
data['Churn'] = LabelEncoder().fit_transform(data['Churn'])

encoded_data = data.copy()
categorical_columns = encoded_data.select_dtypes(include='object').columns.drop('customerID')
for col in categorical_columns:
    encoded_data[col] = LabelEncoder().fit_transform(encoded_data[col])

X = encoded_data.drop(columns=['customerID', 'Churn'])
y = encoded_data['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

scaler = StandardScaler()
numeric_features = ['MonthlyCharges', 'TotalCharges', 'tenure']
X_train[numeric_features] = scaler.fit_transform(X_train[numeric_features])
X_test[numeric_features] = scaler.transform(X_test[numeric_features])

model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

results = {
    'model': 'Gradient Boosting Classifier',
    'accuracy': f'{accuracy:.2%}',
    'recommendation': "Customers with month-to-month contracts and high monthly charges are more likely to churn. Offer discounts or switch them to annual plans.",
    'classification_report': report
}

@app.route('/api/report')
def get_result():   
    return jsonify(results) 

