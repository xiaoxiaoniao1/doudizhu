# -*- coding: utf-8 -*-
# Created by: Vincentzyx
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import time


def EnvToOnehot(cards):
    Env2IdxMap = {3:0,4:1,5:2,6:3,7:4,8:5,9:6,10:7,11:8,12:9,13:10,14:11,17:12,20:13,30:14}
    cards = [Env2IdxMap[i] for i in cards]
    Onehot = torch.zeros((4,15))
    for i in range(0, 15):
        Onehot[:cards.count(i),i] = 1
    return Onehot

def RealToOnehot(cards):
    RealCard2EnvCard = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4,
                        '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9,
                        'K': 10, 'A': 11, '2': 12, 'X': 13, 'D': 14}
    cards = [RealCard2EnvCard[c] for c in cards]
    Onehot = torch.zeros((4,15))
    for i in range(0, 15):
        Onehot[:cards.count(i),i] = 1
    return Onehot


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(60, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 512)
        self.fc4 = nn.Linear(512, 512)
        self.fc5 = nn.Linear(512, 512)
        self.fc6 = nn.Linear(512, 1)
        self.dropout5 = nn.Dropout(0.5)
        self.dropout3 = nn.Dropout(0.3)
        self.dropout1 = nn.Dropout(0.1)

    def forward(self, input):
        x = self.fc1(input)
        x = torch.relu(self.dropout3(self.fc2(x)))
        x = torch.relu(self.dropout5(self.fc3(x)))
        x = torch.relu(self.dropout5(self.fc4(x)))
        x = torch.relu(self.dropout5(self.fc5(x)))
        x = self.fc6(x)
        return x


net = Net()
net.eval()
if os.path.exists("landlord_weights.pkl"):
    net.load_state_dict(torch.load('landlord_weights.pkl'))
else:
    print("landlord_weights.pkl not found")

def predict(cards):
    cards_onehot = torch.flatten(RealToOnehot(cards))
    y_predict = net(cards_onehot)
    return y_predict[0].item() * 100