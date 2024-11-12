import mesa
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
from agent import ChargingStation, Obstacle, Trash, Roomba

class RoombaModel(mesa.Model):
    def __init__(self, width, height, n_agents, dirt_density, obstacle_density, max_time):
        self.width = width
        self.height = height
        self.n_agents = n_agents
        self.max_time = max_time
        self.current_step = 0
        self.running = True
        
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        
        # Calculate number of cells for each type
        n_dirt = int(width * height * dirt_density)
        n_obstacles = int(width * height * obstacle_density)
        
        # Create empty positions list
        all_positions = [(x, y) for x in range(width) for y in range(height)]

        charging_positions = [(1, 1)]
        all_positions.remove((1, 1))

        # Place charging stations
        for i, pos in enumerate(charging_positions):
            station = ChargingStation(f"station_{i}", self)
            self.grid.place_agent(station, pos)
            self.schedule.add(station)
        
        # Place obstacles
        obstacle_positions = self.random.sample(all_positions, n_obstacles)
        for pos in obstacle_positions:
            all_positions.remove(pos)
            obstacle = Obstacle(f"obstacle_{len(self.schedule.agents)}", self)
            self.grid.place_agent(obstacle, pos)
            self.schedule.add(obstacle)
        
        # Place dirt
        dirt_positions = self.random.sample(all_positions, n_dirt)
        for pos in dirt_positions:
            dirt = Trash(f"dirt_{len(self.schedule.agents)}", self)
            self.grid.place_agent(dirt, pos)
            self.schedule.add(dirt)
        
        # Place Roombas

        roomba = Roomba(f"roomba_{0}", self, charging_positions[0])
        self.grid.place_agent(roomba, charging_positions[0])
        self.schedule.add(roomba)

        self.datacollector = DataCollector(
            model_reporters={
                "Step": lambda m: m.current_step,
                "Clean_Percentage": lambda m: self.get_clean_percentage(),
                "Total_Moves": lambda m: self.get_total_moves()
            },
            agent_reporters={
                "Battery": lambda a: getattr(a, "battery", None),
                "Moves": lambda a: getattr(a, "moves_count", None),
                "State": lambda a: getattr(a, "state", None)
            }
        )
    
    def get_clean_percentage(self):
        dirt_count = sum(1 for agent in self.schedule.agents if isinstance(agent, Trash))
        total_cells = self.width * self.height
        return ((total_cells - dirt_count) / total_cells) * 100
    
    def get_total_moves(self):
        return sum(agent.moves_count for agent in self.schedule.agents if isinstance(agent, Roomba))
    
    def step(self):
        self.current_step += 1
        self.schedule.step()
        self.datacollector.collect(self)
        
        if self.current_step >= self.max_time:
            self.running = False