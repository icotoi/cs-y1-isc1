from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class StigmergyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.secrets = []
        self.secret = self.random.randrange(100)
        self.secrets.append(self.secret)

        print("Agent {} Secret {} Len {}".format(self.unique_id, self.secret, len(self.secrets)))

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(self.pos,
                                                          moore=True,
                                                          include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def leave_info(self) -> None:
        self.model.grid.leave_secret(self.pos, self.secret)

    def search_info(self) -> None:
        local_secrets = self.model.grid.read_secrets(self.pos)
        for secret in local_secrets:
            if secret not in self.secrets:
                self.secrets.append(secret)

    def step(self) -> None:
        self.move()
        self.leave_info()
        self.search_info()
        print("Agent {} Secret {} Num secrets: {}".format(self.unique_id, self.secret, len(self.secrets)))

    @property
    def num_secrets(self):
        return len(self.secrets)

    @property
    def max_secrets(self):
        return self.model.num_agents


class StorageGrid(MultiGrid):
    def __init__(self, width: int, height: int, torus: bool) -> None:
        super().__init__(width, height, torus)
        self.grid_crumbs = [[[] for x in range(width)] for y in range(height)]
        print(self.grid_crumbs)

    def leave_secret(self, pos, s):
        x, y = pos
        if s not in self.grid[x][y]:
            self.grid_crumbs[x][y].append(s)

    def read_secrets(self, pos):
        x, y = pos
        return self.grid_crumbs[x][y]


class StigmergyModel(Model):
    def __init__(self, n, width, height):
        self.num_agents = n
        self.grid = StorageGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            m = StigmergyAgent(i, self)
            self.schedule.add(m)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(m, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={'Secrets': 'num_secrets'}
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self) -> None:
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self, n) -> None:
        for i in range(n):
            self.step()
