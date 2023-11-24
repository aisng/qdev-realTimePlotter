import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


def draw(length):
    plt.title("Data")
    plt.xlabel("x")
    plt.ylabel("y")

    x = 0
    for i in range(length):
        y = random.randint(0, 10)
        x += random.randint(1, 10)
        plt.plot(x, y, "bo", linewidth=2, markersize=3, linestyle="solid")

        # plt.pause(1)
    plt.show()


draw(5)
