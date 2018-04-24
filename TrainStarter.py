import sys
from netlang import functional
from netlang.core import Scope, Args, compile
from netlang.data_provider import Batch
from netlang.dataset import mnist
from netlang.module.activation import ReLU, Softmax
from netlang.module.conv import Conv2d, MaxPool2d
from netlang.module.linear import Linear
from netlang.module.loss import CrossEntropy
from netlang.module.metric import OneHot, Accuracy
from netlang.module.noise import NoiseConv2d, NoiseLinear
from netlang.module.optimizer import SGD
from netlang.module.structure import Sequential
from netlang.preprocess import cast
from netlang.module.round import Round


#input argv order
# 0: this file path
# 1: net type
# 2: batch size
# 3: epoch
# 4: output net path
# 5: original net path

#1 types:       mlp  lenet  lenetnoise

#5 original net
#5 mlp           original_net.load('./data/mnist-500-100.npz')
#5 lenet         none
#5 lenetnoise    orignal_net.load('./data/mnist-lenet.npz')


# sample
#c:\python27\python TrainStarter.py lenetnoise 100 2 c:/simulatorProject/XPEControl/mlpout c:/simulatorProject/XPEsim-master/sim_examples/data/mnist-lenet.npz

# c:\python27\python TrainStarter.py lenet 100 2 c:/simulatorProject/XPEControl/mlpout c:/simulatorProject/XPEsim-master/sim_examples/data/mnist-500-100.npz

#c:\python27\python TrainStarter.py mlp 100 2 c:/simulatorProject/XPEControl/mlpout 
#        c:/simulatorProject/XPEsim-master/sim_examples/data/mnist-500-100.npz

type = sys.argv[1] 
batch = sys.argv[2]
epoch_num = sys.argv[3]
output = sys.argv[4]
if type!="lenet":
    original = sys.argv[5]

if type == "mlp":
    original_net = Sequential([
        Linear([784, 500]), ReLU(),
        Linear([500, 100]), ReLU(),
        Linear([100, 10]), Softmax()
    ], name='mnist-500-100')

    try:
        original_net.load(original)
    except:
        pass

    net = Sequential([
        NoiseLinear(original_net.submodule('Linear0'), weight_bits=8, noise=0.07,name='NoiseLinear0'), ReLU(),
        NoiseLinear(original_net.submodule('Linear1'), weight_bits=8, noise=0.07,name='NoiseLinear1'), ReLU(),
        NoiseLinear(original_net.submodule('Linear2'), weight_bits=8, noise=0.07,name='NoiseLinear2'), Softmax()
    ], name='mnist-500-100')

    x = functional.placeholder('x', dims=2)
    y = functional.placeholder('y', dims=1, dtype='int32')

    y_ = net.forward(x)

    loss = CrossEntropy().minimize(y_, OneHot(10).turn(y))
    accuracy = Accuracy().measure(y_, y)

    updates = SGD(learning_rate=0.1, momentum=0.9).updates(net.parameters(), net.differentiate(loss))

    train_op = compile(inputs=[x, y], outputs=[accuracy], updates=updates)
    test_op = compile(inputs=[x, y], outputs=[accuracy])

    batch_size = int(batch)

    train_set = mnist.subset('train')
    train_provider = Batch(train_set, batch_size, y_preprocess=[cast('int32')])

    print('Start training process')
    sys.stdout.flush() 
    for epoch in xrange(int(epoch_num)):
        train_accuracies = []
        for i in xrange(60000 // batch_size):
            x, y = train_provider.get()
            accuracy, = train_op(x, y)
            train_accuracies.append(accuracy)
        train_accuracy = sum(train_accuracies) / len(train_accuracies)

        test_set = mnist.subset('test')
        test_provider = Batch(test_set, batch_size, y_preprocess=[cast('int32')])
        test_accuracies = []
        for j in xrange(10000 // batch_size):
            x, y = test_provider.get()
            accuracy, = test_op(x, y)
            test_accuracies.append(accuracy)
        test_accuracy = sum(test_accuracies) / len(test_accuracies)

        print('Epoch %d, train_accuracy %0.5f, test_accuracy %0.5f' % (epoch, train_accuracy, test_accuracy))
        sys.stdout.flush() 
        net.save(output)

elif type ==  "lenet":
    with Scope(Args(padding='valid')):
        net = Sequential([
            Conv2d([20, 1, 5, 5]), ReLU(), MaxPool2d([2, 2], 2),
            Conv2d([50, 20, 5, 5]), ReLU(), MaxPool2d([2, 2], 2),
            Linear([800, 1250]), ReLU(),
            Linear([1250, 120]), ReLU(),
            Linear([120, 10]), Softmax()
        ], name='mnist-lenet')
    x = functional.placeholder('x', dims=2)
    y = functional.placeholder('y', dims=1, dtype='int32')

    y_ = net.forward(functional.reshape(x, (-1, 1, 28, 28)))

    loss = CrossEntropy().minimize(y_, OneHot(10).turn(y))
    accuracy = Accuracy().measure(y_, y)

    updates = SGD(learning_rate=0.05, momentum=0.9).updates(net.parameters(), net.differentiate(loss))

    print('Begin compile')
    train_op = compile(inputs=[x, y], outputs=[accuracy], updates=updates)
    print('Compiled train_op')
    test_op = compile(inputs=[x, y], outputs=[accuracy])
    print('Compiled test_op')
    batch_size = int(batch)

    train_set = mnist.subset('train')
    train_provider = Batch(train_set, batch_size, y_preprocess=[cast('int32')])

    print('Start training')
    sys.stdout.flush() 
    for epoch in xrange(int(epoch_num)):
        train_accuracies = []
        for i in xrange(60000 / batch_size):
            x, y = train_provider.get()
            accuracy, = train_op(x, y)
            train_accuracies.append(accuracy)
        train_accuracy = sum(train_accuracies) / len(train_accuracies)

        test_set = mnist.subset('test')
        test_provider = Batch(test_set, batch_size, y_preprocess=[cast('int32')])
        test_accuracies = []
        for j in xrange(10000 / batch_size):
            x, y = test_provider.get()
            accuracy, = test_op(x, y)
            test_accuracies.append(accuracy)
        test_accuracy = sum(test_accuracies) / len(test_accuracies)

        print('Epoch %d, train_accuracy %0.5f, test_accuracy %0.5f' % (epoch, train_accuracy, test_accuracy))
        sys.stdout.flush() 
        net.save(output)
        
elif type ==  "lenetnoise":

    weight_bits = 8
    io_bits = 8
    noise = 0.03

    with Scope(Args(padding='valid')):
        orignal_net = Sequential([
            Conv2d([20, 1, 5, 5]), ReLU(), MaxPool2d([2, 2], 2),
            Conv2d([50, 20, 5, 5]), ReLU(), MaxPool2d([2, 2], 2),
            Linear([800, 1250]), ReLU(),
            Linear([1250, 120]), ReLU(),
            Linear([120, 10]), Softmax()
        ], name='mnist-lenet')
    orignal_net.load(original)
    with Scope(Args(padding='valid', weight_bits=weight_bits, io_bits=io_bits, noise=noise)):
        net = Sequential([
            NoiseConv2d(orignal_net.submodule('Conv2d0')), Round(), MaxPool2d([2, 2], 2),
            NoiseConv2d(orignal_net.submodule('Conv2d1')), Round(), MaxPool2d([2, 2], 2),
            NoiseLinear(orignal_net.submodule('Linear0')), Round(),
            NoiseLinear(orignal_net.submodule('Linear1')), Round(),
            NoiseLinear(orignal_net.submodule('Linear2')), Softmax()
        ], name='mnist-lenet.low')

    x = functional.placeholder('x', dims=2)
    y = functional.placeholder('y', dims=1, dtype='int32')

    y_ = net.forward(functional.reshape(x, (-1, 1, 28, 28)))

    loss = CrossEntropy().minimize(y_, OneHot(10).turn(y))
    accuracy = Accuracy().measure(y_, y)

    updates = SGD(learning_rate=0.05, momentum=0.9).updates(net.parameters(), net.differentiate(loss))+ net.updates()

    print('Begin compile')
    train_op = compile(inputs=[x, y], outputs=[accuracy], updates=updates)
    print('Compiled train_op')
    test_op = compile(inputs=[x, y], outputs=[accuracy])
    print('Compiled test_op')
    batch_size = int(batch)

    train_set = mnist.subset('train')
    train_provider = Batch(train_set, batch_size, y_preprocess=[cast('int32')])

    print('Start training')
    sys.stdout.flush() 
    testa=[]
    for epoch in xrange(int(epoch_num)):
        train_accuracies = []
        for i in xrange(60000 / batch_size):
            x, y = train_provider.get()
            accuracy, = train_op(x, y)
            train_accuracies.append(accuracy)
        train_accuracy = sum(train_accuracies) / len(train_accuracies)

        test_set = mnist.subset('test')
        test_provider = Batch(test_set, batch_size, y_preprocess=[cast('int32')])
        test_accuracies = []
        for j in xrange(10000 / batch_size):
            x, y = test_provider.get()
            accuracy, = test_op(x, y)
            test_accuracies.append(accuracy)
        test_accuracy = sum(test_accuracies) / len(test_accuracies)
        testa.append(test_accuracy)
        print('Epoch %d, train_accuracy %0.5f, test_accuracy %0.5f' % (epoch, train_accuracy, test_accuracy))
        sys.stdout.flush() 
        net.save(output)

