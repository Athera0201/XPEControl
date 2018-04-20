import simulator
import numpy as np
import sys
import os
#input argv order
# 0: this file path
# 1: weights file path
# 2: image file path
# 3: batch size
# 4: net type   cnn/mlp 
# 5: config file path

#cnn original path
#weights_dir = "./data/mnist-lenet.npz" 
#image_dir = "./data/dataset/mnist/test.npy"

#mlp original path
#weights_dir = "./data/mnist-500-100.npz" 
#image_dir = "./data/dataset/mnist/test.npy"

#sample:
# c:\python27\python SimStarter.py C:/simulatorProject/XPEsim-master/sim_examples/data/mnist-lenet.npz C:/
#			simulatorProject/XPEsim-master/sim_examples/data/dataset/mnist/test.npy 10 cnn C:/simulatorProject/XPEControl

weights_dir = sys.argv[1] 
image_dir = sys.argv[2]
batch_size = int(sys.argv[3]) # The number of input picture
weights = np.load(weights_dir)['arr_0'].item()
data = np.load(image_dir)[:batch_size]
images = data[:, 0]
labels = data[:, 1]


os.chdir(sys.argv[5]) 
params = simulator.Parameterinput() # Read parameters in simconfig

if sys.argv[4] == "cnn":
    # Define the neural network
    net = [
        ['Conv2d',],
        ['Conv2d',],
        ['Linear',],
        ['Linear',],
        ['Linear',],
    ]
elif sys.argv[4] == "mlp":
    # Define the neural network
    net = [
        ['Linear'],
        ['Linear'],
        ['Linear']
    ]

	
# SIM
HWsim = simulator.SystemSim(params) 
HWsim.apply(net, weights, images, labels) # Forward computing
HWsim.HWEvaluate()
HWsim.show() # Show the result in console
