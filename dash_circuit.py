import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pennylane as qml
from pennylane import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Quantum circuit
def quantum_circuit(angle):
    dev = qml.device("default.qubit", wires=1)

    @qml.qnode(dev)
    def circuit():
        qml.RY(angle, wires=0)
        return qml.probs(wires=[0])

    return circuit()

# Layout for the app
app.layout = html.Div([
    html.H1("Interactive Quantum Circuit Visualizer"),
    dcc.Slider(
        id="angle-slider",
        min=0,
        max=2 * np.pi,
        step=0.1,
        value=np.pi / 4,
        marks={0: "0", np.pi: "π", 2 * np.pi: "2π"},
    ),
    dcc.Graph(id="probability-graph")
])

# Callback for updating the graph
@app.callback(
    Output("probability-graph", "figure"),
    [Input("angle-slider", "value")]
)
def update_graph(angle):
    probs = quantum_circuit(angle)
    fig = go.Figure(data=[
        go.Bar(x=["|0⟩", "|1⟩"], y=probs, marker=dict(color=["blue", "orange"]))
    ])
    fig.update_layout(
        title=f"Quantum State Probabilities (Angle = {angle:.2f} rad)",
        xaxis_title="State",
        yaxis_title="Probability",
        yaxis=dict(range=[0, 1])
    )
    return fig

# Expose the app for Gunicorn
server = app.server
