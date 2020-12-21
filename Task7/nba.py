import random
import pandas as pd


# P(B/A)
def get_p(symptoms, test_symptom):
    def _float(x):
        return x if isinstance(x, float) else float(x.replace(',', '.'))

    p = 1
    for i, symptom in enumerate(symptoms):
        # Обработка когда симптом есть и нет
        p *= _float(symptom) if test_symptom[i] == 1 else (1 - _float(symptom))
    return p


def get_answer(disease, symptoms, test_symptom):
    # P(A/B) = P(B/A) * P(A) / P(B)
    max_v, answer = None, None
    for index, (dis, p_a) in enumerate(disease.items(), start=1):
        symptom_p = get_p(symptoms.iloc[::, index][1:], test_symptom)
        if max_v is None or max_v < symptom_p * p_a:
            max_v = symptom_p * p_a
            answer = dis

    return answer


symptoms = pd.read_csv(
    'symptom.csv',
    delimiter=';'
)
diseases = pd.read_csv(
    'disease.csv',
    delimiter=';'
)

# Формирование P(A)
disease = dict(
    zip(list(diseases['Болезнь'][:len(diseases) - 1]),
        list(diseases['Случаев'][:len(diseases) - 1] / diseases['Случаев'][len(diseases) - 1]))
)

test_symptom = [
    random.randint(0, 1) for i in range(len(symptoms) - 1)
]

print(f'Результат: {get_answer(disease, symptoms, test_symptom)}')
