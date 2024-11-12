from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from model import roomba
from agent import Roomba, Trash, Obstacle

def agent_portrayal(agent):
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
        "y": agent.pos[1]
    }
    
    if isinstance(agent, Roomba):
        portrayal["Color"] = "#000000"  # Black
    elif isinstance(agent, Trash):
        portrayal["Color"] = "#00FF00"  # Green
    elif isinstance(agent, Obstacle):
        portrayal["Color"] = "#FF0000"  # Red
    else:
        portrayal["Color"] = "#FFFFFF"  # Default to white if agent type is unknown
    
    return portrayal

# Crear elementos de visualización
canvas_element = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

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
    roomba,
    [canvas_element, chart],
    "Cellular Automata",
    model_params
)

if __name__ == "__main__":
    server.launch()