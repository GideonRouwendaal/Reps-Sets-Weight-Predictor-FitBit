import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

## Formulas based on https://en.wikipedia.org/wiki/One-repetition_maximum#Calculating_1RM

def epley_formula(number_of_reps, weight_lifted_in_set):
    return weight_lifted_in_set * (1 + number_of_reps / 30)


def brzycki_formula(number_of_reps, weight_lifted_in_set):
    return weight_lifted_in_set / (1.0278 - (0.0278 * number_of_reps))


def mcGlothin_formula(number_of_reps, weight_lifted_in_set):
    return 100 * weight_lifted_in_set / (101.3 - (2.67123 * number_of_reps))


def lombardi(number_of_reps, weight_lifted_in_set):
    return weight_lifted_in_set * (number_of_reps ** 0.1)


def oconner_et_al(number_of_reps, weight_lifted_in_set):
    return weight_lifted_in_set * (1 + number_of_reps / 40)

def calculate_1RM(number_of_reps, weight_lifted_in_set):
    if weight_lifted_in_set == 0:
        weight_lifted_in_set = 1
    return (epley_formula(number_of_reps, weight_lifted_in_set) + brzycki_formula(number_of_reps, weight_lifted_in_set)
            + mcGlothin_formula(number_of_reps, weight_lifted_in_set) + lombardi(number_of_reps, weight_lifted_in_set) +
            oconner_et_al(number_of_reps, weight_lifted_in_set)) / 5

def create_list_1RM(data):
    result = []
    number_of_sets = len(data)
    counter = 0
    for i in range(1, len(data[0])):
        if result[-1] == result[-2] == [-3] and len(result):
            result.pop()
            result.pop()
            print("yes")
            return result                                           # provide adding not-filled in cells
        temp = 0
        amount_nan = 0
        for j in range(number_of_sets):
            if data[j][i] == data[j][i]:                            # if set does not contain a value NaN
                temp += data[j][i]
            else:                                                   # if set does contain NaN --> no value, increase amount_NaN by 1
                amount_nan += 1
        if (number_of_sets - amount_nan) == 0:                      # if 1 day is missed, use the last value and add it to the result
            if len(result) > 0:                                     # if there is previous data available
                average = result[-1]
                result.append(average)
            else:
                result.append(0)                                    # if the exercise have not been performed (no data)
        else:
            temp /= (number_of_sets - amount_nan)
            if counter % 2 == 0:
                result.append(temp)
            else:
                average_1RM = calculate_1RM(result[-1], temp)
                result.pop()
                result.append(average_1RM)
        counter += 1
    return result


def generate_data(data):
    test_result = []
    temp = []
    for i in range (len(data)):
        if "SET" not in data[i][0]:
            if temp != []:
                test_result.append(np.array(create_list_1RM(temp)))
            test_result.append(data[i][0])
            temp = []
        else:
            temp.append(data[i])
        if i == len(data) - 1:
            test_result.append(np.array(create_list_1RM(temp)))
    return test_result


def plateau_func(x, a, b, c):
    return a*np.log2(b+x)+2*c


def create_graph(data):
    plot = plt
    plot.xlabel('Number of weeks training')
    plot.ylabel('Estimated weight for 1RM')
    for i in range(int(len(data) / 2)):
        label = data[i*2]
        y = data[i*2+1]
        x = list(range(1, len(y) + 1))
        popt, pcov = curve_fit(plateau_func, x, y)
        plt.scatter(x, y, label="Original Data" + label)
        x = list(range(1, len(y) + 25))
        plt.plot(x, plateau_func(x, *popt), 'r-', label="Fitted Curve" + label)
    plot.legend()
    plot.show()


# https://towardsdatascience.com/how-to-use-data-to-gain-insights-from-workout-routines-c700e2e59859

# data = pd.read_excel("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/Plateau predictor/testData1.xlsx", engine='openpyxl')
# relevant_data = pd.DataFrame(data)
# relevant_data = (relevant_data.values)
#
# cleaned_data = generate_data(relevant_data)
# create_graph(cleaned_data)
#
#
# data = pd.read_excel("C:/Users/gideo/Google Drive/Documenten-b/Self Study/Python/Fitness/Plateau predictor/testBenchData.xlsx", engine='openpyxl')
# relevant_data = pd.DataFrame(data)
# relevant_data = (relevant_data.values)