import random
import math
def train_test_split(x, y, test_size):
    if(len(x) != len(y)):
        return "data size are unequal"
    
    l = len(x)
    test_len = math.ceil(l*test_size)
    x_test = []
    y_test = []
    for i in range(test_len):
        idx = random.randint(0,l-1)
        x_test.append(x.pop(idx))
        y_test.append(y.pop(idx))
        l -= 1

    return x, x_test, y, y_test


x = [random.randint(1, 10) for i in range(10)]
y = [random.randint(1, 10) for i in range(10)]
print("x=",x)
print("y=",y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
print("x_train=",x_train)
print("y_train=",y_train)
print("x_test=",x_test)
print("y_test=",y_test)