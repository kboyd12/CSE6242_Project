from src.viz.frontend.view import create_plot
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=create_plot())])

app.run_server(debug=True, use_reloader=False)
