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

# Updated chart configurations
clean_chart = ChartModule(
    [{"Label": "Clean_Percentage", "Color": "#00FF00"}],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500
)

time_chart = ChartModule(
    [{"Label": "Time_To_Clean", "Color": "#FF0000"}],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500
)

moves_chart = ChartModule(
    [{"Label": "Total_Moves", "Color": "#0000FF"}],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500
)

model_params = {
    "width": 50,
    "height": 50,
    "n_agents": Slider("Number of Roombas", 1, 1, 5, 1),
    "dirt_density": Slider("Dirt Density", 0.3, 0.0, 1.0, 0.1),
    "obstacle_density": Slider("Obstacle Density", 0.1, 0.0, 1.0, 0.1),
    "max_time": NumberInput("Maximum Steps", 1000)
}

# Updated server configuration with new charts
server = ModularServer(
    RoombaModel,
    [canvas_element, clean_chart, time_chart, moves_chart],
    "Roomba Simulation",
    model_params
)

if __name__ == "__main__":
    server.launch()