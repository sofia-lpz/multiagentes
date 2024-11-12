# server.py
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, NumberInput
from agent import ChargingStation, Obstacle, Trash, Roomba
from model import RoombaModel

def agent_portrayal(agent):
    if agent is None:
        return
        
    portrayal = {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0
    }
    
    if isinstance(agent, Roomba):
        portrayal["Color"] = "#000000"  # Black
        portrayal["Layer"] = 2
    elif isinstance(agent, Trash):
        portrayal["Color"] = "#00FF00" # Green
        portrayal["Layer"] = 1
    elif isinstance(agent, Obstacle):
        portrayal["Color"] = "#FF0000"  # Red
        portrayal["Layer"] = 1
    elif isinstance(agent, ChargingStation):
        portrayal["Color"] = "#FFFF00"  # Yellow
        portrayal["Layer"] = 1
    
    return portrayal

# Create visualization elements
canvas_element = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

charts = [
    ChartModule([
        {"Label": "Clean_Percentage", "Color": "#00FF00"}
    ]),
    ChartModule([
        {"Label": "Total_Moves", "Color": "#0000FF"}
    ])
]

# Model parameters
model_params = {
    "width": 50,
    "height": 50,
    "n_agents": 1,
    "dirt_density": Slider("Dirt Density", 0.3, 0.0, 1.0, 0.1),
    "obstacle_density": Slider("Obstacle Density", 0.1, 0.0, 1.0, 0.1),
    "max_time": NumberInput("Maximum Steps", 1000)
}

# Create and launch server
server = ModularServer(
    RoombaModel,
    [canvas_element] + charts,
    "Roomba Simulation",
    model_params
)

if __name__ == "__main__":
    server.launch()