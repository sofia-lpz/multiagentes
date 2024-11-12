import mesa
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import Roomba, Trash, Obstacle

class roomba(mesa.Model):
    def __init__(self, width=50, height=50, density=0.5):
        self.grid = SingleGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

        num_obstacles = int(width * density)
        obstacle_positions = self.random.sample([(x, y) for x in range(width) for y in range(height)], num_obstacles)

        num_dirt = int(width * density)
        dirt_positions = self.random.sample([(x, y) for x in range(width) for y in range(height)], num_dirt)

        for y in range(height-1, -1, -1):  
            for x in range(width):

                if (x, y) in obstacle_positions:
                    agent = Obstacle((x, y), self)
                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

                if (x, y) in dirt_positions and (x, y) not in obstacle_positions:
                    agent = Trash((x, y), self)
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
        self.datacollector.collect(self)