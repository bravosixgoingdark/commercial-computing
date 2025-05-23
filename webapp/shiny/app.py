from faicons import icon_svg
import plotly.graph_objects as go
from shinywidgets import render_widget
from shared import app_dir, df
from shiny import reactive
from shiny.express import input, render, ui
import requests
import json
from pprint import pformat

ui.page_opts(fillable=True)

ui.include_css(app_dir / "styles.css")

ui.input_dark_mode(mode="dark")

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("users")):
        "Number of Customers"
        @render.text
        def total_customers():
            return f"{len(df):,}"

    with ui.value_box(showcase=icon_svg("money-bill")):
        "Total Monthly Bill ($)"
        @render.text
        def total_bill():
            return f"${df['MonthlyCharges'].sum():,.2f}"

    with ui.value_box(showcase=icon_svg("chart-bar")):
        "Average Churn Rate (%)"
        @render.text
        def avg_churn_rate():
            churn_rate = (df['Churn'].value_counts(normalize=True).get('Yes', 0) * 100)
            return f"{churn_rate:.2f}%"

with ui.layout_columns():
    with ui.card(full_screen=True):
        with ui.navset_card_underline():
            with ui.nav_panel("Churn Distribution"):
                @render_widget
                def churn_distribution():
                    churn_data = df['Churn'].value_counts(normalize=True) * 100

                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=churn_data.index,
                        y=churn_data.values,
                        text=[f"{val:.1f}%" for val in churn_data.values],
                        textposition="outside"
                    ))
                    fig.update_layout(
                        xaxis_title="Churn",
                        yaxis_title="Percentage",
                        yaxis=dict(range=[0, 100])
                    )
                    fig.update_layout(
                        template="plotly_dark"
                    )
                    return fig

            with ui.nav_panel("Churn Insights"):
                @render_widget
                def vs_churn_chart():
                    monthly_data = df.groupby(['MonthlyCharges_Bin', 'Churn']).size().unstack(fill_value=0)
                    internet_data = df.groupby(['InternetService', 'Churn']).size().unstack(fill_value=0)
                    contract_data = df.groupby(['Contract', 'Churn']).size().unstack(fill_value=0)
                    tenure_data = df.groupby(['Tenure_Bin', 'Churn']).size().unstack(fill_value=0)
                    security_data = df.groupby(['OnlineSecurity', 'Churn']).size().unstack(fill_value=0)

                    fig = go.Figure()

                    fig.add_trace(go.Bar(
                        x=monthly_data.index,
                        y=monthly_data['Yes'],
                        name="Churned (Yes)",
                        marker_color="#EF553B",
                        visible=True  
                    ))
                    fig.add_trace(go.Bar(
                        x=monthly_data.index,
                        y=monthly_data['No'],
                        name="Not Churned (No)",
                        marker_color="#636EFA",
                        visible=True 
                    ))

                    # Internet Service
                    fig.add_trace(go.Bar(
                        x=internet_data.index,
                        y=internet_data['Yes'],
                        name="Churned (Yes)",
                        marker_color="#EF553B",
                        visible=False
                    ))
                    fig.add_trace(go.Bar(
                        x=internet_data.index,
                        y=internet_data['No'],
                        name="Not Churned (No)",
                        marker_color="#636EFA",
                        visible=False
                    ))

                    # Contract
                    fig.add_trace(go.Bar(
                        x=contract_data.index,
                        y=contract_data['Yes'],
                        name="Churned (Yes)",
                        marker_color="#EF553B",
                        visible=False
                    ))
                    fig.add_trace(go.Bar(
                        x=contract_data.index,
                        y=contract_data['No'],
                        name="Not Churned (No)",
                        marker_color="#636EFA",
                        visible=False
                    ))

                    # Tenure
                    fig.add_trace(go.Bar(
                        x=tenure_data.index,
                        y=tenure_data['Yes'],
                        name="Churned (Yes)",
                        marker_color="#EF553B",
                        visible=False
                    ))
                    fig.add_trace(go.Bar(
                        x=tenure_data.index,
                        y=tenure_data['No'],
                        name="Not Churned (No)",
                        marker_color="#636EFA",
                        visible=False
                    ))

                    # Online Security
                    fig.add_trace(go.Bar(
                        x=security_data.index,
                        y=security_data['Yes'],
                        name="Churned (Yes)",
                        marker_color="#EF553B",
                        visible=False
                    ))
                    fig.add_trace(go.Bar(
                        x=security_data.index,
                        y=security_data['No'],
                        name="Not Churned (No)",
                        marker_color="#636EFA",
                        visible=False
                    ))

                    fig.update_layout(
                        updatemenus=[
                            dict(
                                buttons=[
                                    dict(label="Monthly Charges",
                                         method="update",
                                         args=[{"visible": [True, True, False, False, False, False, False, False, False, False]},
                                               {"xaxis": {"title": "Monthly Charges Range"},
                                                "yaxis": {"title": "Customer Count"}}]),
                                    dict(label="Internet Service",
                                         method="update",
                                         args=[{"visible": [False, False, True, True, False, False, False, False, False, False]},
                                               {"xaxis": {"title": "Internet Service Type"},
                                                "yaxis": {"title": "Customer Count"}}]),
                                    dict(label="Contract",
                                         method="update",
                                         args=[{"visible": [False, False, False, False, True, True, False, False, False, False]},
                                               {
                                                "xaxis": {"title": "Contract Type"},
                                                "yaxis": {"title": "Customer Count"}}]),
                                    dict(label="Tenure",
                                         method="update",
                                         args=[{"visible": [False, False, False, False, False, False, True, True, False, False]},
                                               {
                                                "xaxis": {"title": "Tenure Range (Months)"},
                                                "yaxis": {"title": "Customer Count"}}]),
                                    dict(label="Online Security",
                                         method="update",
                                         args=[{"visible": [False, False, False, False, False, False, False, False, True, True]},
                                               {
                                                "xaxis": {"title": "Online Security Status"},
                                                "yaxis": {"title": "Customer Count"}}]),
                                ],
                                direction="down",
                                showactive=True
                            )
                        ],
                        xaxis=dict(title="Monthly Charges Range"),  
                        yaxis=dict(title="Customer Count"),  
                        barmode="stack"
                    )
                    fig.update_layout(template="plotly_dark")

                    return fig
            with ui.nav_panel("Churn prediction API"):
                @render.code
                def api_response():
                    try:
                        response = requests.get("http://churnapp.mooo.com:5000/api/report")  # Replace with your API endpoint
                        response.raise_for_status()
                        data = response.json()
                        output = f"""
                            Model: {data['model']}
                            Accuracy: {data['accuracy']}
                            
                            Classification Report:
                            - Class 0: 
                              * Precision: {data['classification_report']['0']['precision']}
                              * Recall: {data['classification_report']['0']['recall']}
                              * F1-Score: {data['classification_report']['0']['f1-score']}
                              * Support: {data['classification_report']['0']['support']}
                              
                            - Class 1:
                              * Precision: {data['classification_report']['1']['precision']}
                              * Recall: {data['classification_report']['1']['recall']}
                              * F1-Score: {data['classification_report']['1']['f1-score']}
                              * Support: {data['classification_report']['1']['support']}
                              
                            Macro Average:
                            - Precision: {data['classification_report']['macro avg']['precision']}
                            - Recall: {data['classification_report']['macro avg']['recall']}
                            - F1-Score: {data['classification_report']['macro avg']['f1-score']}
                            - Support: {data['classification_report']['macro avg']['support']}
                            
                            Weighted Average:
                            - Precision: {data['classification_report']['weighted avg']['precision']}
                            - Recall: {data['classification_report']['weighted avg']['recall']}
                            - F1-Score: {data['classification_report']['weighted avg']['f1-score']}
                            - Support: {data['classification_report']['weighted avg']['support']}
                            
                            Recommendation:
                            {data['recommendation']}
                        """
                        return output 
                    except requests.exceptions.RequestException as e:
                        return f"Error fetching data from API: {e}"
