#!/usr/bin/env python3
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return 1 + (1 / N) - 2 * B


class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth += 1
            self.wealth -= 1

    def step(self) -> None:
        # print("agent {}".format(self.unique_id))
        self.move()
        if self.wealth > 0:
            self.give_money()


class MoneyModel(Model):
    def __init__(self, n, width, height):
        self.num_agents = n
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            m = MoneyAgent(i, self)
            self.schedule.add(m)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(m, (x, y))

        self.datacollector = DataCollector(
            model_reporters={'Gini': compute_gini},
            agent_reporters={'Wealth': 'wealth'}
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self) -> None:
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self, n) -> None:
        for i in range(n):
            self.step()
