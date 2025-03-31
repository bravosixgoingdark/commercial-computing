import seaborn as sns

from shared import df
from shiny.express import input, render, ui

ui.page_opts(title=ui.h2("Phototype app", class_="pt-5"))
ui.nav_spacer()

with ui.nav_panel("Churn rate"):
    with ui.navset_card_underline(title="Customer churn distrubution"):
        with ui.nav_panel("Plot"):
            @render.plot
            def hist():
                p = sns.histplot(df, x='Churn', facecolor="#007bc2", edgecolor="white")
                return p.set(xlabel='Customer churn distrubution')
        with ui.nav_panel("Table"):
            @render.data_frame
            def data():
                return df[["customerID", "Churn"]]

with ui.nav_panel("Churn rate by contract"):
    with ui.navset_card_underline(title="Churn rate by contract type"):
        with ui.nav_panel("Plot"):
            @render.plot
            def churn_contract():
                p = sns.countplot(x='Contract', hue='Churn', data=df, palette='coolwarm') 
                return p.set(xlabel='Contract Type', ylabel='Count')                      
        with ui.nav_panel("Table"):                                                     
            @render.data_frame                                                          
            def churn_data():                                                                 
                return df[["customerID", "Churn", "Contract"]]                                      
