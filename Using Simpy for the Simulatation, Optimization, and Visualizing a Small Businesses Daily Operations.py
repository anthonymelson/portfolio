import simpy as simpy
import numpy as np
import pandas as pd
import random as random
import math as math
import itertools

"""
THIS IS A TOOL TO EXPLORE FUNCTIONS FOR CUSTOMER GENERATION RATES

i = 0
x = 0
time = []
cust = []
while i < 28800:
    fun = lambda x: -(x*4 -0.00015*x**2)/1000 +60
    Rate = fun(i)
    time.append(i)
    cust.append(Rate)
    i = i + 1
    x = x + 1
plt.plot(time, cust)
plt.ylabel('Customers Served')
plt.xlabel('Potential Customers')
plt.show()

"""


"""

Define:
        Work Process (Customer Arrives, Decides on Order, THEN, Employee Takes Order, Shaves Ice, Adds Flavor, and Rings Them Out)
        Useable Objects/Resources (Ice_Machine, Register, Employees)
        Stocks/Containers (Ice, Flavors)
        Thier Relations in the Enviornment

"""


def Shaved_Ice_Stand(Ice_Machines, Employee, Register, Set_Seed):

    random.seed(a=Set_Seed)
    i = 0

    Revenue = []
    Machine_Wait_Time = []
    Cash_Register_Wait_Time = [0]
    Time_Per_Customer = [0]
    Potential_Customers = []
    Served_Customers = []

    def Potential_Customer(env, Employees, Ice_Machine, Cash_Register, Ice_Fridge):
        Rate = lambda x: -(x*5 -0.00015*x**2)/2000 +60
        for i in itertools.count():
            t = i

            if len(Employees.queue) < 4:
                env.process(Service_Counter_Operation(env,Employees, Ice_Machine, Cash_Register, t, Ice_Fridge))

            Current_Time = env.now
            Customer_Rate = math.floor(Rate(Current_Time))
            yield env.timeout(Customer_Rate)

            Potential_Customers.append([1])

    def Service_Counter_Operation(env, Employees, Ice_Machine, Cash_Register, t, Ice_Fridge):
            t = t

            with Employees.request() as Assign_Employee:
                yield Assign_Employee

                Customer_Decision_Time = random.uniform(10, 25)
                Sale_Amount = np.random.choice(4, 1, p=[0.0,0.6,0.3,0.1])
                yield env.timeout(Customer_Decision_Time)

                Use_Machine = Ice_Machine.request()
                Use_Machine_Time = random.uniform(30, 50) + (Sale_Amount * 2)
                yield Use_Machine
                yield env.timeout(Use_Machine_Time)
                Ice_Machine.release(Use_Machine)

                Add_Flavor_Time = random.uniform(15, 20)
                yield env.timeout(Add_Flavor_Time)

                Use_Cash_Register = Cash_Register.request()
                Take_Payment_Time = random.uniform(10, 15)
                yield Use_Cash_Register
                yield env.timeout(Take_Payment_Time)
                Cash_Register.release(Use_Cash_Register)

                Revenue.append([Sale_Amount])
                Served_Customers.append([1])

                yield Ice_in_Machine.get(1)

                if Ice_in_Machine.level < 3:
                    yield Ice_Fridge.get(1)
                    yield Ice_in_Machine.put(17)
                    yield env.timeout(10)

                if Ice_Fridge.level < 3:
                    yield Ice_Fridge.put(7)
                    yield env.timeout(300)

    env = simpy.Environment(initial_time=0)

    Ice_Machine = simpy.Resource(env, capacity=Ice_Machines)
    Employees = simpy.Resource(env, capacity=Employee)
    Cash_Register = simpy.Resource(env, capacity = Register)

    Ice_in_Machine = simpy.Container(env,capacity=20, init=17)
    Ice_Fridge = simpy.Container(env, capacity=10, init=7)

    simpy.Process(env, Potential_Customer(env, Employees, Ice_Machine, Cash_Register, Ice_Fridge))
    env.run(until=28800)

    Total_Revenue = sum(Revenue)
    Total_Served = sum(Served_Customers)

    return Total_Revenue, Total_Served




"""

Every Combination Up To Four, Where Registers =< Employees AND Ice_Machines =< Employees (29 Possible). Others
Are Left Out because Equal or Greater Number of Personnel Are Needed To Use All of a Resource Type Simultaneously.

"""
Decision_Set = [[1,1,1,i], [1,2,1,i], [1,3,1,i], [1,4,1,i],
                [2,2,1,i], [2,3,1,i], [2,4,1,i], [3,3,1,i],
                [3,4,1,i], [4,4,1,i], [1,2,2,i], [1,3,2,i],
                [1,4,2,i], [1,3,3,i], [1,4,3,i], [1,4,4,i],
                [2,2,2,i], [2,3,2,i], [2,4,2,i], [2,3,3,i],
                [2,4,3,i], [2,4,4,i], [3,3,2,i], [3,4,2,i],
                [3,3,3,i], [3,4,3,i], [3,4,4,i], [4,4,3,i],
                [4,4,4,i]]

"""

Simulate Each Solution Set N-Times, Record Average Revenues of Each, Calculate Costs of Settings, and Store in DF.

"""


n = 0
Final_Results = []
while n < len(Decision_Set):

    i = 0
    Revenue_Collected = []
    Simulations_Per_Decision_Set = 3

    while i < Simulations_Per_Decision_Set:

        Revenue, Total_Served = Shaved_Ice_Stand(Decision_Set[n][0], Decision_Set[n][1], Decision_Set[n][2],Decision_Set[n][3])
        Revenue_Collected.append([Revenue])
        i = i + 1

    Avg_Revenue = sum(Revenue_Collected)/Simulations_Per_Decision_Set

    Material_Cost = Total_Served * 0.25
    Labor_Cost = Decision_Set[n][1] *8 * 20
    Machine_Cost = Decision_Set[n][0] * 50
    Register_Cost = Decision_Set[n][2] * 25
    Total_Cost = Material_Cost + Labor_Cost + Machine_Cost + Register_Cost

    Profit = Avg_Revenue - Total_Cost

    Final_Results.append([Decision_Set[n], Labor_Cost, Machine_Cost, Register_Cost, Total_Cost, Avg_Revenue, Profit])

    n = n + 1

Results_Table = pd.DataFrame(Final_Results,
                columns=['Decision_Set', 'Labor_Cost', 'Machine_Cost', 'Register_Cost', 'Total_Cost', 'Avg_Revenue', 'Profit'])
"""

Find Optimal Solution Set

"""
Highest_Profit = Results_Table['Profit'].idxmax()
Optimal_Solution_Set = Decision_Set[Highest_Profit]

print(Optimal_Solution_Set, '  ', max
