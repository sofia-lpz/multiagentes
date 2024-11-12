# server.py
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, NumberInput
from model import RoombaModel
from agent import Roomba, Trash, Obstacle, ChargingStation

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
        portrayal["Color"] = "#00FF00"  # Green
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

# Updated chart configuration
clean_chart = ChartModule(
    [{"Label": "Clean_Percentage", "Color": "#00FF00"}],  # Changed from Clean Percentage
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500
)

moves_chart = ChartModule(
    [{"Label": "Total_Moves", "Color": "#0000FF"}],  # Changed from Total Moves
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500
)

battery_chart = ChartModule(
    [{"Label": "Average_Battery", "Color": "#FF0000"}],  # Changed from Average Battery
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500
)

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
    [canvas_element, clean_chart, moves_chart, battery_chart],
    "Roomba Simulation",
    model_params
)

if __name__ == "__main__":
    server.launch()