import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('fivethirtyeight')


state = [300,1000,500]

transition = [

            [0.2, 0.7, 0.1],
            [0.3, 0.1, 0.6],
            [0.6, 0.2, 0.2]

                            ]

stateHistory = []
stateTrack = [state]
last_state = []
i = 0
length = [0]
convergence = False

while convergence == False and i < 10:
    last_state = state
    state = np.dot(state, transition)
    stateTrack.append(list(state))
    i = i + 1
    length.append(i)

    if all(last_state == state) == True:
        convergence = True

"""
for s in range(len(stateTrack[0])):
    plt.plot(length, [states[s] for states in stateTrack], label= 'Company %s' %s)
plt.legend()
plt.show()
"""

dims =(10.7, 7.27)
fig, ax = pyplot.subplots(figsize=dims)
splot = pd.DataFrame(stateTrack, length, ["Company 1", "Company 2", "Company 3"])
sns.lineplot(ax=ax, data = splot, markers=True)
"""
splot = pd.DataFrame(stateTrack, length, ["Company 1", "Company 2", "Company 3"])
ax = sns.lineplot(data=splot,style="event",lw=2, markers=True)
"""
print('')
print('Converged in', i, 'Iterations')
print('')
print('Steady State Vector: ', state)
