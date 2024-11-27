import numpy as np
def getclases():
    final_classes = []
    with open('classes.txt', 'r') as file:
        for line in file:
            final_classes.append(line.strip())
            np.random.seed(42)
    return final_classes
