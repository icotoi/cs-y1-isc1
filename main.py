#!/usr/bin/env python3
import numpy as np

from money import MoneyModel
import matplotlib.pyplot as plt


m = MoneyModel(50, 10, 10)

for i in range(20):
    m.step()

agent_counts = np.zeros((m.grid.width, m.grid.height))
for cell in m.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()
plt.show()
