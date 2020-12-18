import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("dataset/train.csv")

plt.xlabel('Class')
plt.ylabel('Passangers count')
plt.title('Class/Passengers')

data.Pclass.hist(color=(0, 0, 1))

plt.show()