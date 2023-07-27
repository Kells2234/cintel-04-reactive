""" 
Purpose: Provide reactive output for the MT Cars dataset.

- Use inputs from the UI Sidebar to filter the dataset.
- Update reactive outputs in the UI Main Panel.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

"""
import pathlib
from shiny import render, reactive
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
from shinywidgets import render_widget
import plotly.express as px

from util_logger import setup_logger

logger, logname = setup_logger(__name__)


def get_mtcars_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    p = pathlib.Path(__file__).parent.joinpath("data").joinpath("mtcars.csv")
    # logger.info(f"Reading data from {p}")
    original_df = pd.read_csv(p)
    total_count = len(original_df)

    reactive_df = reactive.Value()

    @reactive.Effect
    @reactive.event(
        input.MTCARS_MPG_RANGE,
        input.MT_CARS_MAX_HP,
    )
    def _():
        df = original_df.copy()

        input_range = input.MTCARS_MPG_RANGE()
        input_min = input_range[0]
        input_max = input_range[1]

        """
        Filter the dataframe to just those greater than or equal to the min
        and less than or equal to the max
        Note: The ampersand (&) is the Python operator for AND
        The column name is in quotes and is "mpg".
        You must be familiar with the dataset to know the column names.
        """

        df = [(df["mpg"] >= input_min) & (df["mpg"] <= input_max) & (df["hp"] <= input.MT_CARS_MAX_HP()) ]

        # Set the reactive value
        reactive_df.set(df)

    @output
    @render.text
    def mtcars_record_count_string():
        filtered_df = reactive_df.get()
        filtered_count = len(filtered_df)
        message = f"Showing {filtered_count} of {total_count} records"
        # logger.debug(f"filter message: {message}")
        return message

    @output
    @render.table
    def mtcars_filtered_table():
        filtered_df = reactive_df.get()
        return filtered_df

    @output
    @render_widget
    def mtcars_output_widget1():
        df = reactive_df.get()
        plotly_express_plot = px.scatter(df, x="mpg", y="hp", color="cyl", size="wt")
        plotly_express_plot.update_layout(title="MT Cars with Plotly Express")
        return plotly_express_plot

    @output
    @render.plot
    def mtcars_plot1():
        df = reactive_df.get()
        matplotlib_fig, ax = plt.subplots()
        plt.title("MT Cars with matplotlib")
        ax.scatter(df["wt"], df["mpg"])
        return matplotlib_fig

    @output
    @render.plot
    def mtcars_plot2():
        df = reactive_df.get()
        plotnine_plot = (
            ggplot(df, aes("wt", "mpg"))
            + geom_point()
            + ggtitle("MT Cars with plotnine")
        )

        return plotnine_plot

    # return a list of function names for use in reactive outputs
    return [
        mtcars_record_count_string,
        mtcars_filtered_table,
        mtcars_output_widget1,
        mtcars_plot1,
        mtcars_plot2,
    ]
