# agent.py
import mesa
import numpy as np

class ChargingStation(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        pass

class Obstacle(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        pass

class Trash(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        pass

class Roomba(mesa.Agent):
    def __init__(self, unique_id, model, home_station_pos, battery=100):
        super().__init__(unique_id, model)
        self.battery = battery
        self.home_station_pos = home_station_pos
        self.moves_count = 0
        self.state = "exploring"  # exploring, charging, returning
        
    def get_neighbors(self):
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        return neighbors
    
    def move_to(self, new_pos):
        if self.battery > 0:
            self.model.grid.move_agent(self, new_pos)
            self.battery -= 1
            self.moves_count += 1
            return True
        return False
    
    def find_path_to(self, target_pos):
        current_x, current_y = self.pos
        target_x, target_y = target_pos
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        
        best_step = None
        min_distance = float('inf')
        
        for step in possible_steps:
            cell_contents = self.model.grid.get_cell_list_contents(step)
            if any(isinstance(agent, Obstacle) for agent in cell_contents):
                continue
                
            distance = abs(step[0] - target_x) + abs(step[1] - target_y)
            if distance < min_distance:
                min_distance = distance
                best_step = step
                
        return best_step
    
    def step(self):
        if self.battery <= 20 and self.state != "charging":
            self.state = "returning"
            
        if self.state == "charging":
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            if any(isinstance(obj, ChargingStation) for obj in cell_contents):
                self.battery = min(100, self.battery + 5)
                if self.battery >= 100:
                    self.state = "exploring"
            return
            
        if self.state == "returning":
            next_pos = self.find_path_to(self.home_station_pos)
            if next_pos:
                self.move_to(next_pos)
                if self.pos == self.home_station_pos:
                    self.state = "charging"
            return
            
        #limpiar
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        trash = [obj for obj in cell_contents if isinstance(obj, Trash)]
        if trash:
            self.model.grid.remove_agent(trash[0])
            self.model.schedule.remove(trash[0])
            self.battery -= 1
            return
            
        # moverse toma energia?
        possible_moves = self.get_neighbors()
        valid_moves = []
        for move in possible_moves:
            cell_contents = self.model.grid.get_cell_list_contents([move])
            if not any(isinstance(agent, (Obstacle, Roomba)) for agent in cell_contents):
                valid_moves.append(move)
                
        if valid_moves:
            new_pos = self.random.choice(valid_moves)
            self.move_to(new_pos)
            self.battery -= 1