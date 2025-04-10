from faicons import icon_svg
import plotly.express as px

from shinywidgets import render_widget

# Import data from shared.py
from shared import app_dir, df
from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Penguins dashboard", fillable=True)


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of customers"

        @render.text
        def count():
            return df.shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average montly customer bill"

        @render.text
        def bill_length():
            return f"{df['MonthlyCharges'].mean():.1f}"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"something"


with ui.layout_columns():
    with ui.card(full_screen=True):
        with ui.navset_card_underline():
            with ui.nav_panel("Churn rate"):
                with ui.layout_columns():
                    @render_widget
                    def churn_rate():
                        churn = px.histogram(df, x=input.var1(), y='Churn', color=input.var1(), histfunc='avg')
                        churn.update_yaxes(title_text='Churn rate')
                        return churn
                with ui.layout_columns():
                     ui.input_select("var1", None, choices=["Contract", "InternetService"], width="100%")

            with ui.nav_panel("Churn Distribution"):
                with ui.layout_columns():
                    @render_widget
                    def churn_distribution():
                        distribution = px.histogram(df.replace({'Churn': {0: 'Yes', 1: 'No'}}), y='PaymentMethod', color='Churn')
                        distribution.update_xaxes(title_text='Number of Customers')
                        distribution.update_yaxes(title_text='Payment Method')
                        return distribution
            with ui.nav_panel("Charges Distribution"):
                with ui.layout_columns():
                    @render_widget
                    def charges_distribution():
                        distribution = px.box(df.replace({'Churn': {0: 'Yes', 1: 'No'}}), x='Churn', y='MonthlyCharges')
                        distribution.update_xaxes(title_text='Churn Status')
                        distribution.update_yaxes(title_text='Monthly Charges')
                        return distribution
            with ui.nav_panel("Tenure Distribution"):
                with ui.layout_columns():
                    @render_widget
                    def tenure_distribution():
                        distribution = px.histogram(df.replace({'Churn': {0: 'Yes', 1: 'No'}}), x='tenure', color='Churn', barmode='stack', nbins=30)
                        distribution.update_xaxes(title_text='Tenure (Months)')
                        distribution.update_yaxes(title_text='Number of Customers')
                        return distribution



    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = ['customerID', 
                    'PhoneService', 
                    'MultipleLines', 
                    'InternetService', 
                    'StreamingTV', 
                    'StreamingMovies', 
                    'Contract', 
                    'PaperlessBilling', 
                    'PaymentMethod', 
                    'MonthlyCharges', 
                    'TotalCharges'
                    ]
            return render.DataGrid(df[cols], filters=True)


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
