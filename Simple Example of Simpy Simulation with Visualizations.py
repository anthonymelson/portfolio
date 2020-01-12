from simpy import events
import random
import simpy
import math as math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
#plt.style.use('fivethirtyeight')
#print(plt.style.available)
#plt.style.use(['seaborn-notebook'])

def run():
    new_customer = 200
    interval = 10
    line_depth = [0]
    customers_served = [0]
    potential_customers = [0]
    customer_rate = [0]
    time = [0]
    served = []
    unserved = []
    ts = []
    tus = []


    def parabolaFunc(i):
        return ((i - new_customer/2)**2)/new_customer

    def sinFunc(i):
        return abs(math.log(math.sin(i/20)))

    def logFunc(i):
        return math.log(i**3)



    def new_buyer(env,buyer,stand,new):
        for i in range(new):
            #Buyer Process
            b = buyer(env,stand, i+1, trans_time=50)
            env.process(b)
            #Distribution for Customer Frequency
            upper_bound = parabolaFunc(i) + 5
            lower_bound = upper_bound - 5
            t = random.uniform(lower_bound,upper_bound)
 #           t = random.expovariate(5)*5
            #Time between Customers/Time Passage
            time.append(env.now)

            yield env.timeout(t)


    def buyer(env,stand, name, trans_time):
        #Tracking Customer Arrival and Line Length
        arrive = round(env.now,2)
        in_line = stand.count
        line_depth.append(in_line)
        #Request place in line, Acceptable length == Capacity of Resource
        with stand.request() as req:
            results = yield req | env.timeout(0)

            if req in results:
#                print('name:',name,'  Arrived: ', arrive, '   In Line:',in_line, '  Stayed')
#                print('  ')
                #Monitoring Potential and Served Customers who Stayed
                potential_customers.append(sum(potential_customers[-1])+1)
                customers_served.append(sum(customers_served[-1])+1)
                #Time to Service a Customer
                yield env.timeout(trans_time)
                #Tracking Finished Service
                served.append([1])

#                print('Customer', name, 'Finished')
#                print(' ')

            else:
#                print('name:',name, '  Arrived: ', arrive, '   In Line:', in_line, '  Left')
#                print('  ')
                #Tracking Potential and Served for those that left
                potential_customers.append(sum(potential_customers[-1])+1)
                customers_served.append(sum(customers_served[-1]))
                #Counting Unserved Customers
                unserved.append([1])

            total_served = sum(served)
            total_unserved = sum(unserved)
            ts.append(total_served)
            tus.append(total_unserved)
    #Envornment at t=1, resource at capacity=5, and process of Customers passing and staying
    env = simpy.Environment(initial_time=1)
    stand = simpy.Resource(env, capacity=5)
    env.process(new_buyer(env, buyer,stand,new_customer))
    env.run(until=15000)

    #Plot Potential Customers vs Customers Served against Time
    plt.plot(time, potential_customers, label='Potential')
    plt.plot(time, customers_served, label='Served')
    plt.ylabel('Customers')
    plt.xlabel('Time')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.show()
    #Plotting Potential Customers and Customers Served against eachother
    plt.plot(potential_customers, customers_served)
    plt.ylabel('Customers Served')
    plt.xlabel('Potential Customers')
    plt.show()
    #Plotting Line Length vs Potential Customers
    plt.plot(potential_customers, line_depth)
    plt.ylabel('Line_Length')
    plt.xlabel('Potential Customers')
    plt.show()
    #Plotting Line Length vs Time
    plt.plot(time, line_depth)
    plt.ylabel('Line_Length')
    plt.xlabel('Time')
    plt.show()

    print('Served: ', sum(served))
    print('Unserved: ', sum(unserved))
    print('Percent Served: ', sum(served)/sum(served + unserved))

    return ts, tus

run()
