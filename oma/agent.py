import mesa

class CellAgent(mesa.Agent):
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
        
        # Si es la fila superior, mantiene su estado
        if y == self.model.grid.height - 1:
            self.next_state = self.state
            return
            
        # Obtiene el patrón de los vecinos superiores
        neighbors = self.get_top_neighbors()
        
        self.next_state = (not neighbors[0] and neighbors[2]) or (neighbors[0] and not neighbors[2]) 
    
    def advance(self):
        if self.next_state is not None:
            self.state = self.next_state
            self.next_state = None

