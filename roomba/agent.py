import mesa

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
    def __init__(self, unique_id, model, battery=100):
        super().__init__(unique_id, model)
        self.battery = battery
        self.next_state = None
        
    def get_neighbors(self):
        """
        Obtiene las celdas vecinas.
        """
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        
        return neighbors
    
    def step(self):
        """
        Calcula el siguiente estado basado en los vecinos superiores.
        """
        x, y = self.pos
        
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        trash = [obj for obj in this_cell if isinstance(obj, Trash)]

        if len(trash) > 0:
            self.next_state = True
            return
        
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid.remove_agent(sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)
    
    def advance(self):
        if self.next_state is not None:
            self.state = self.next_state
            self.next_state = None

