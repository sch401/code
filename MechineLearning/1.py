import pandas as pd
import torch
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.nn import init
import random
from sklearn.preprocessing import MinMaxScaler

seed=0

random.seed(seed)
np.random.seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

# Remove randomness (may be slower on Tesla GPUs) 
# https://pytorch.org/docs/stable/notes/randomness.html
if seed == 0:
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False



Sourcedata = pd.read_excel('MLAD_SourceData (1).xlsx',sheet_name='Sheet2')
print(Sourcedata)
Sd0 = Sourcedata.drop(index=[])                                                 #  删除了数据
Sd1 = Sd0.to_numpy()

standardScaler = MinMaxScaler()
standardScaler.fit(Sd1)
Sd = standardScaler.transform(Sd1)

A = Sd[0:135,2:10]
b = Sd[0:135,10]
C = Sd[135:,2:10]
d = Sd[135:,10]
x = torch.from_numpy(A).to(torch.float32)
y = torch.from_numpy(b).to(torch.float32)
x_test = torch.from_numpy(C).to(torch.float32)
y_test = torch.from_numpy(d).to(torch.float32)


class simpleNet(nn.Module):
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(simpleNet, self).__init__()
        self.layer1 = nn.Linear(in_dim, n_hidden_1)
        self.layer2 = nn.Linear(n_hidden_1, n_hidden_2)
        self.layer3 = nn.Linear(n_hidden_2, out_dim)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x
    
class Activation_Net(nn.Module):
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(Activation_Net, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1),nn.ReLU())
        self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.ReLU())
        self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, out_dim))

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

 # 1. 根据网络层的不同定义不同的初始化方式     
def weight_init(net):
    for m in net.modules():
        if isinstance(m, nn.Conv2d):
            init.xavier_uniform(m.weight)
            if m.bias:
                init.constant(m.bias, 0.5)
        elif isinstance(m, nn.BatchNorm2d):
            init.constant(m.weight, 1)
            init.constant(m.bias, 0.5)
        elif isinstance(m, nn.Linear):
            init.normal(m.weight)
            # if m.bias:
            #    init.constant(m.bias, 0)


# 2. 初始化网络结构        
net = Activation_Net(8,6,3,1)
# 3. 将weight_init应用在子模块上

net.apply(weight_init)
optimizer = torch.optim.Adamax(net.parameters(),lr = 0.001)
loss_func = torch.nn.MSELoss()

plt.ion()
plt.show()
epoch = 14000
for t in range(epoch):
    prediction1 = net(x)
    prediction1 = prediction1.squeeze(-1)
    loss1 = loss_func(prediction1,y)
    #print("Epoch {}, loss: {}".format(t, loss1))
    optimizer.zero_grad()
    loss1.backward()
    optimizer.step()
    if t % 200 == 0:  # 每100步打印一次损失
        prediction2 = net(x_test)
        loss2 = loss_func(prediction2,y_test)
        print('Epoch:{}, loss1:{:.6f}'.format(t, loss2))
        plt.cla()
        plt.scatter(prediction2.data.numpy(), y_test.data.numpy())
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
        # plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)
        plt.text(0.5, 0, 'Loss = %.4f' % loss2.data, fontdict={'size': 20, 'color': 'red'})
        plt.pause(0.05) 
print(y_test.data.numpy)
plt.ioff()
plt.show()


#0.05
