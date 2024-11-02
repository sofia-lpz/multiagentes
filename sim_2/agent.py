import mesa

class CellAgent(mesa.Agent):
    def __init__(self, unique_id, model, initial_state=False):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.next_state = None
        
    def get_top_neighbors(self):
        x, y = self.pos
        neighbors_states = []

        top_y = (y + 1) % self.model.grid.height
        
        for dx in [-1, 0, 1]:
            nx = (x + dx) % self.model.grid.width

            cell = self.model.grid.get_cell_list_contents([(nx, top_y)])
            if cell:
                neighbors_states.append(1 if cell[0].state else 0)
            else:
                neighbors_states.append(0)
                
        return neighbors_states
    
    def step(self):
        neighbors = self.get_top_neighbors()

        self.next_state = (not neighbors[0] and neighbors[2]) or (neighbors[0] and not neighbors[2])
    
    def advance(self):
        if self.next_state is not None:
            self.state = self.next_state
            self.next_state = None