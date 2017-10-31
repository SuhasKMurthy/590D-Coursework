import math
from random import randint
import numpy as np
import matplotlib.pyplot as plt

#number of stream elements
num_elements = 1000000

element_max_value = 1000

#'a' coefficients for hash family
a = []
#'b' coefficients for hash family
b = []

#p is a prime number that is greater than max possible value of x
p = 104729

#number of hash functions
n = 25

def generate_hash_func_coefficients():
    global a, b
    for i in range(n):
        x = ((p - 2)/(n + 1)) * (i + 1)
        y = (p - 1)/n * i

        a.append(int(x))
        b.append(int(y))

    b.reverse()


def hash_value(x, ai, bi, m):
    return ((ai * x + bi)%p)%m

def get_min_freq(cms, x, m):
    min_val = num_elements + 1
    for i in range(n):
        y = hash_value(x, a[i], b[i], m)
        val = cms[i][y]
        if val < min_val:
            min_val = val
    return min_val

def plot_freq(dict_true_freq, dict_cms_freq):
    plt.title('Frequency of Elements: Count Min sketch vs True Frequencies', fontsize=12)
    plt.xlabel('Element')
    plt.ylabel('Frequency')
    line_actual, = plt.plot(list(dict_true_freq.keys()), list(dict_true_freq.values()))
    line_cms, = plt.plot(list(dict_cms_freq.keys()), list(dict_cms_freq.values()))
    plt.legend((line_actual, line_cms), ('Actual frequency', 'CMS frequency'))
    #plt.show()

generate_hash_func_coefficients()
#print(a)
#print(b)

def count_min_sketch(eps):
    # number of buckets
    l = math.ceil(1 / eps)

    dict_true_freq = {}
    dict_cms_freq = {}

    cms = np.zeros(shape=(n, l))
    # print(cms)

    #initialize true frequency counts of each element to 0
    for i in range(element_max_value):
        dict_true_freq[i+1] = 0

    for i in range(num_elements):
        x = randint(1, element_max_value)

        value = dict_true_freq.get(x)
        dict_true_freq[x] = value + 1

        for j in range(n):
            freq = hash_value(x, a[j], b[j], l)
            val = cms[j][freq]
            cms[j][freq] = val + 1


    print(dict_true_freq)

    for i in range(element_max_value):
        x = get_min_freq(cms, i + 1, l)
        dict_cms_freq[i + 1] = x

    #plot_freq(dict_true_freq, dict_cms_freq)
    return dict_true_freq, dict_cms_freq

    #print(cms)
    #print(dict_cms_freq)

# error
dict_true_freq_1, dict_cms_freq_1 = count_min_sketch(0.01)
dict_true_freq_2, dict_cms_freq_2 = count_min_sketch(0.0001)

plt.figure(1)
plt.title('Frequency of Elements: Count Min sketch vs True Frequencies (eps = 0.01)', fontsize=12)
plt.xlabel('Element')
plt.ylabel('Frequency')
line_actual, = plt.plot(list(dict_true_freq_1.keys()), list(dict_true_freq_1.values()))
line_cms, = plt.plot(list(dict_cms_freq_1.keys()), list(dict_cms_freq_1.values()))
plt.legend((line_actual, line_cms), ('Actual frequency', 'CMS frequency'))

plt.figure(2)

plt.title('Frequency of Elements: Count Min sketch vs True Frequencies (eps = 0.0001)', fontsize=12)
plt.xlabel('Element')
plt.ylabel('Frequency')
line_actual, = plt.plot(list(dict_true_freq_2.keys()), list(dict_true_freq_2.values()))
line_cms, = plt.plot(list(dict_cms_freq_2.keys()), list(dict_cms_freq_2.values()))
plt.legend((line_actual, line_cms), ('Actual frequency', 'CMS frequency'))

plt.show()