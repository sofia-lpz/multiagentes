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

    battery = 100

    def __init__(self, unique_id, model, initial_state=False):
        super().__init__(unique_id, model)
        self.state = initial_state  # True = Alive, False = Dead
        self.next_state = None
        
    def get_top_neighbors(self):
        x, y = self.pos
        neighbors_states = []

        for dx in [-1, 0, 1]:
            nx = (x + dx) % self.model.grid.width  # Horizontal wrapping
            ny = (y + 1) % self.model.grid.height  # Vertical wrapping

            cell = self.model.grid.get_cell_list_contents([(nx, ny)])
            if cell:
                neighbors_states.append(1 if cell[0].state else 0)
            else:
                neighbors_states.append(0)
        return neighbors_states
    
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

