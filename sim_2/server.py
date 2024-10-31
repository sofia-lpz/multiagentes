from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from model import CellularAutomata

def cell_portrayal(agent):
    """
    Define la representación visual de cada celda.
    """
    if agent is None:
        return
        
    portrayal = {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Color": "#000000" if agent.state else "#FFFFFF"
    }
    
    return portrayal

# Crear elementos de visualización
canvas_element = CanvasGrid(cell_portrayal, 50, 50, 500, 500)

chart = ChartModule(
    [
        {"Label": "Alive", "Color": "#D3D3D3"},
        {"Label": "Dead", "Color": "#000000"}
    ]
)

# Configurar y lanzar servidor
model_params = {
    "width": 50,
    "height": 50,
    "density": Slider("Initial Density", 0.5, 0.01, 1.0, 0.01)
}

server = ModularServer(
    CellularAutomata,
    [canvas_element, chart],
    "Cellular Automata",
    model_params
)

if __name__ == "__main__":
    server.launch()