#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Searching over the simulation to find its sensitivity to parameters
#Searching pitch moment weighting of SAE car problem - can alter line 51 to change the weighting. 

import Comms_framework as Comms_framework
import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math


params = {}
params['update_interval'] = 20
params['max_designs'] = 1
params['compiler_iterations'] = 1
params['compiler_starting_samples'] = 1
params['compiler_interval'] = 10
params['max_iterations'] = 1000
params['meeting_length'] = 50
params['reward_scale'] = 1

exploration_phase_fraction = 0.01 #[0.001,0.05,0.1,0.2,0.35,0.500,0.650,0.800,0.900,0.950,1]
#num_iterations = [100,200,500,750,1000]
max_designs = [1,2,3,4,5,7,9,11] #changes the max designs for the simulator

num_tries = 20
num_iterations = params['max_iterations']
#iteration_record = np.zeros((len(exploration_phase_fraction),len(num_iterations),num_tries))
obj_record2 = np.zeros((num_iterations,len(max_designs),num_tries))

for i in range(len(max_designs)):
    exploration_phase_iterations = math.ceil(num_iterations*exploration_phase_fraction)

    params['max_iterations'] = 10000
    max_iterations = num_iterations
    
    params['max_designs'] = max_designs[i]
    params['compiler_iterations'] = 1
    params['compiler_starting_samples'] = max_designs[i]*3

    
    for k in range(num_tries):

        test_framework = Comms_framework.comms_framework(params)
        test_framework.problem.weights[-1] *= 1 #multiplier for pitch moment weight
        
        action = np.zeros(len(test_framework.action_space.high))
        action[0] = 1
        
        print(params['max_designs'])
        if params['max_designs'] == 1:
            
            test_framework.switch_to_integration()

        for j in range(max_iterations):

            if j == exploration_phase_iterations:
                test_framework.switch_to_integration()
                
            old_obj = test_framework.best_solution_value

            test_framework.step(action)

            new_obj = test_framework.best_solution_value
            obj_record2[j,i,k] = new_obj

r_2 = obj_record2
np.save('pitch_moment_00_1',obj_record2)

