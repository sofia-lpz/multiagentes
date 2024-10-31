from mesa.visualization import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

from model import Automata

COLORS = {"Alive": "#666666", "Dead": "#FFFFFF"}

def automata_portrayal(cell):
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}

    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[cell.condition]

    return portrayal

canvas_element = CanvasGrid(automata_portrayal, 50, 50, 500, 500)

cell_chart = ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

model_params = {
    "height": 50,
    "width": 50,
    "density": Slider("Initial Density", 0.5, 0.01, 1.0, 0.01),
}

server = ModularServer(
    Automata, [canvas_element, cell_chart, pie_chart], "Automata", model_params
)

server.launch()