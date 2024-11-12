# model.py
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
        
        # Create empty positions list
        all_positions = [(x, y) for x in range(width) for y in range(height)]
        charging_positions = [(1, 1)]
        all_positions.remove((1, 1))
        
        # Place Roombas and their charging stations first
        self.roombas = []
        
        # Place first Roomba and its charging station
        station = ChargingStation(f"station_0", self)
        self.grid.place_agent(station, charging_positions[0])
        self.schedule.add(station)
        
        roomba = Roomba(f"roomba_0", self, charging_positions[0])
        self.grid.place_agent(roomba, charging_positions[0])
        self.schedule.add(roomba)
        self.roombas.append(roomba)
        
        # Place additional Roombas in random positions
        available_positions = [pos for pos in all_positions]
        for i in range(n_agents - 1):
            if available_positions:
                pos = self.random.choice(available_positions)
                available_positions.remove(pos)
                all_positions.remove(pos)
                
                # Place charging station first at the Roomba's position
                charging_station = ChargingStation(f"station_{i+1}", self)
                self.grid.place_agent(charging_station, pos)
                self.schedule.add(charging_station)
                
                # Create Roomba with its own charging station position
                roomba = Roomba(f"roomba_{i+1}", self, pos)  # Pass this station's position
                self.grid.place_agent(roomba, pos)
                self.schedule.add(roomba)
                self.roombas.append(roomba)
        
        # Calculate number of cells for dirt and obstacles
        n_dirt = int(width * height * dirt_density)
        n_obstacles = int(width * height * obstacle_density)
        
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
        
        self.initial_dirt_count = n_dirt
        
        # Updated datacollector with correct metrics
        self.datacollector = DataCollector(
            model_reporters={
                "Clean_Percentage": self.get_clean_percentage,
                "Total_Moves": self.get_total_moves,
                "Average_Battery": self.get_average_battery
            }
        )
        
        # Collect initial state
        self.datacollector.collect(self)
    
    def get_clean_percentage(self):
        dirt_count = sum(1 for agent in self.schedule.agents if isinstance(agent, Trash))
        return ((self.initial_dirt_count - dirt_count) / self.initial_dirt_count) * 100 if self.initial_dirt_count > 0 else 100
    
    def get_total_moves(self):
        return sum(agent.moves_count for agent in self.roombas)
    
    def get_average_battery(self):
        if not self.roombas:
            return 0
        return sum(agent.battery for agent in self.roombas) / len(self.roombas)
    
    def step(self):
        self.current_step += 1
        self.schedule.step()
        self.datacollector.collect(self)
        
        if self.current_step >= self.max_time:
            self.running = False