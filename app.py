"""
Purpose: Use Python to create a continuous intelligence and 
interactive analytics dashboard using Shiny for Python with 
interactive charts from HoloViews Bokeh and Plotly Express.

Each Shiny app has two parts: 

- a user interface app_ui object (similar to the HTML in a web page) 
- a server function that provides the logic for the app (similar to JS in a web page).

"""
from shiny import App, ui
import shinyswatch

from flights_server import get_flights_server_functions
from flights_ui_inputs import get_flights_inputs
from flights_ui_outputs import get_flights_outputs

from mtcars_server import get_mtcars_server_functions
from mtcars_ui_inputs import get_mtcars_inputs
from mtcars_ui_outputs import get_mtcars_outputs

from penguins_server import get_penguins_server_functions
from penguins_ui_inputs import get_penguins_inputs
from penguins_ui_outputs import get_penguins_outputs

from relationships_server import get_relationships_server_functions
from relationships_ui_inputs import get_relationships_inputs
from relationships_ui_outputs import get_relationships_outputs

from util_logger import setup_logger

logger, logname = setup_logger(__name__)

app_ui = ui.page_navbar(
    shinyswatch.theme.lumen(),
    ui.nav(
        "Flights",
        ui.layout_sidebar(
            get_flights_inputs(),
            get_flights_outputs(),
        ),
    ),
    ui.nav(
        "MT_Cars",
        ui.layout_sidebar(
            get_mtcars_inputs(),
            get_mtcars_outputs(),
        ),
    ),
    ui.nav(
        "Penguins",
        ui.layout_sidebar(
            get_penguins_inputs(),
            get_penguins_outputs(),
        ),
    ),
    ui.nav(
        "Relationships",
        ui.layout_sidebar(
            get_relationships_inputs(),
            get_relationships_outputs(),
        ),
    ),
    ui.nav(ui.a("About", href="https://github.com/Kells2234")),
    ui.nav(ui.a("GitHub", href="https://github.com/Kells2234/cintel-04-reactive")),
    ui.nav(ui.a("App", href="https://s557075ks.shinyapps.io/cintel-04-reactive/")),
    ui.nav(ui.a("Examples", href="https://shinylive.io/py/examples/")),
    ui.nav(ui.a("Widgets", href="https://shiny.rstudio.com/py/docs/ipywidgets.html")),
    title=ui.h1("Kelly Dashboard"),
)


def server(input, output, session):
    """Define functions to create UI outputs."""

    logger.info("Starting server...")
    get_flights_server_functions(input, output, session)
    get_mtcars_server_functions(input, output, session)
    get_penguins_server_functions(input, output, session)
    get_relationships_server_functions(input, output, session)


# app = App(app_ui, server, debug=True)
app = App(app_ui, server)
