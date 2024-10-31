import mesa
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import CellAgent

class CellularAutomata(mesa.Model):
    def __init__(self, width=50, height=50):
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = SimultaneousActivation(self)
        
        # Crear agentes
        for y in range(height-1, -1, -1):  
            for x in range(width):
                agent = CellAgent((x, y), self)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
                
                # Inicializar aleatoriamente la fila superior
                if y == height-1:  
                    agent.state = self.random.choice([True, False])
        
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
