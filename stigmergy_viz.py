#!/usr/bin/env python3
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from stigmergy import StigmergyModel


def agent_portrayal(agent):
    print(agent)
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "text": "K",
        "Text": "{} - {} - {}".format(agent.unique_id, agent.secret, agent.num_secrets)
    }

    if agent.num_secrets < agent.max_secrets:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([{"Label": "Secrets",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(StigmergyModel,
                       [grid, chart],
                       "Stigmergy Model",
                       {
                           "n": 10,
                           "width": 10,
                           "height": 10
                       })
server.port = 8521  # The default
server.launch()
