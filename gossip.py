from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class GossipAgent(Agent):
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

    def gossip(self) -> None:
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.tell_agent(self.secret)

    def tell_agent(self, s) -> None:
        if s not in self.secrets:
            self.secrets.append(s)

    def step(self) -> None:
        self.move()
        self.gossip()
        print("Agent {} Secret {} Num secrets: {}".format(self.unique_id, self.secret, len(self.secrets)))

    @property
    def num_secrets(self):
        return len(self.secrets)

    @property
    def max_secrets(self):
        return self.model.num_agents


class GossipModel(Model):
    def __init__(self, n, width, height):
        self.num_agents = n
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            m = GossipAgent(i, self)
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
