import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("dataset/train.csv")

age_surv = {}

for age, survived in zip(data.Age, data.Survived):
    age_surv[age] = age_surv.get(age, 0) + survived

plt.xlabel('Age')
plt.ylabel('Count of survived')
plt.title('Age/survived')

plt.scatter(age_surv.keys(), age_surv.values())

plt.show()

