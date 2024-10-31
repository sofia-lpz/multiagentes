from mesa import Agent

class Cell(Agent):

    def __init__(self, pos, model):

        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Alive"
        self._next_condition = None

    def step(self):
        if self.condition == "Alive":
            top_neighbor_pos = (self.pos[0], self.pos[1] + 1)
            top_right_neighbor_pos = (self.pos[0] + 1, self.pos[1] + 1)
            top_left_neighbor_pos = (self.pos[0] - 1, self.pos[1] + 1)

            top_neighbor = self.model.grid.get_cell_list_contents([top_neighbor_pos])
            top_right_neighbor = self.model.grid.get_cell_list_contents([top_right_neighbor_pos])
            top_left_neighbor = self.model.grid.get_cell_list_contents([top_left_neighbor_pos])

            if (top_left_neighbor.condition == "Dead" and top_right_neighbor.condition == "Alive") or (top_left_neighbor.condition == "Alive" and top_right_neighbor.condition == "Dead"):
                self._next_condition = "Alive"
            else:
                self._next_condition = "Dead"

    def advance(self):
        if self._next_condition is not None:
            self.condition = self._next_condition