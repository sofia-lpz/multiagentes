import mesa
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import Roomba, Trash, Obstacle

class roomba(mesa.Model):
    def __init__(self, width=50, height=50, density=0.5):
        self.grid = SingleGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.current_row = height - 1

        num_obstacles = int(width * height * 0.1)
        obstacle_positions = self.random.sample(list(self.grid.coord_iter()), num_obstacles)

        for y in range(height-1, -1, -1):  
            for x in range(width):

                if (x, y) in obstacle_positions:
                    agent = Obstacle((x, y), self)
                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

        
        self.datacollector = DataCollector(
            {
                "Alive": lambda m: sum(1 for a in m.schedule.agents if a.state),
                "Dead": lambda m: sum(1 for a in m.schedule.agents if not a.state)
            }
        )
        
        self.running = True
    def step(self):
        # solo se actualiza una fila por step
        self.datacollector.collect(self)
        row_agents = [agent for agent in self.schedule.agents if agent.pos[1] == self.current_row]
        for agent in row_agents:
            agent.step()
        
        for agent in row_agents:
            agent.advance()
        
        self.current_row -= 1
        if self.current_row < 0:
            self.current_row = self.grid.height - 1