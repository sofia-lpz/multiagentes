import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation

from agent import Cell

class Automata(Model):
    
    def __init__(self, height=50, width=50, density=0.5):

        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead"),
            }
        )

        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                new_cell = Cell((x, y), self)

                if x == 0:
                    new_cell.condition = "Alive"

                self.grid.place_agent(new_cell, (x, y))
                self.schedule.add(new_cell)

        self.running = True
        self.datacollector.collect(self)
    
    def step(self):
        self.schedule.step()
        
        self.datacollector.collect(self)

        if self.count_type(self, "Alive") == 0:
            self.running = False

    
    @staticmethod
    def count_type(model, cell_condition):
        return sum([1 for cell in model.schedule.agents if cell.condition == cell_condition])