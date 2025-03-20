import seaborn as sns

# Import data from shared.py
from shared import df
from shiny.express import input, render, ui

# Page title (with some additional top padding)
ui.page_opts(title=ui.h2("Phototype app", class_="pt-5"))


# Render a histogram of the selected variable (input.var())
@render.plot
def hist():
    p = sns.histplot(df, x='Churn', facecolor="#007bc2", edgecolor="white")
    return p.set(xlabel='Customer churn distrubution')


