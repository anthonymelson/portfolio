# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 13:40:15 2020

@author: Anthony Melson
"""
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

N = 12 # Number of Machines
machine_probs = np.random.uniform(low=0.4, high=0.8, size=N).round(2) # Win Probability of Machines
rounds = 500 # Total Plays
wins = np.zeros(N) #Tracks Wins for Each Machine
losses = np.zeros(N) # Tracks Losses for Each Machine
total_reward = 0 # Tracks Overall Wins for All Rounds
machine_played = [] # Tracks Total Plays for Each Machine

# Iterate Through Rounds
for i in range(0, rounds):
    probs = np.zeros(N) # Store Each Machine's Draw to be Played
    # Iterate Through Machines
    for machine in range(0, N):
        probs[machine] = random.betavariate(wins[machine] + 1, losses[machine] + 1) # Draw Based on Previous Results and Randomness

    selected_machine = np.argmax(probs) # Machine With Best Draw
    machine_played.append(selected_machine) # Collect Machine With Best Draw
    
    # Simulate Playing the Selected Machine, and Collect Reward
    reward = np.random.choice([0,1],1, p = [1 - machine_probs[selected_machine], machine_probs[selected_machine]])
    
    # Count Wins, Losses, and Reward
    if reward == 1:
        wins[selected_machine] = wins[selected_machine] + 1
    else:
        losses[selected_machine] = losses[selected_machine] + 1
    total_reward = total_reward + reward

# Create and Print DataFrame with Wins, Losses, and Probabilities of Machine
df = pd.DataFrame(wins, columns=['Wins'])
df['Losses'] = losses
df['Actual Probability'] = machine_probs
print(df)
print()
print(f"Machine {np.argmax(wins)} won most, with {int(wins[np.argmax(wins)])} wins")
print(f"Total Reward: {total_reward[0]}")

# Plot Histogram of Total Plays For Each Machine
plt.hist(machine_played)
plt.title('Histogram of Machine Plays')
plt.xlabel('Machines')
plt.ylabel('Number of Times Selected')
plt.show()



