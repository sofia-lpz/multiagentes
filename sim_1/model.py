import mesa
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import CellAgent

class CellularAutomata(mesa.Model):
    def __init__(self, width=50, height=50, density=0.5):
        self.grid = SingleGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

        num_alive_cells = int(width * density)
        first_row_positions = [(x, height-1) for x in range(width)]
        alive_positions = self.random.sample(first_row_positions, num_alive_cells)

        for y in range(height-1, -1, -1):  
            for x in range(width):
                agent = CellAgent((x, y), self)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
                
                if y == height-1:
                    agent.state = (x, y) in alive_positions
                else:
                    agent.state = False
        
        self.datacollector = DataCollector(
            {
                "Alive": lambda m: sum(1 for a in m.schedule.agents if a.state),
                "Dead": lambda m: sum(1 for a in m.schedule.agents if not a.state)
            }
        )
        
        self.running = True
        
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()