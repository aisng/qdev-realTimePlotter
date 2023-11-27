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

        plt.pause(1)
    plt.show()


draw(5)

# x = [40, 72, 45]
# y = [42, 61, 85]
# # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
# fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
# ax.plot(x, y, label='linear')  # Plot some data on the axes.
#
# ax.set_xlabel('x label')  # Add an x-label to the axes.
# ax.set_ylabel('y label')  # Add a y-label to the axes.
# ax.set_title("Simple Plot")  # Add a title to the axes.
# ax.legend()  # Add a legend.
# plt.show()


# plt.xlim(0, len(x_vals))
# plt.ylim(0, len(y_vals))
# for i in range(10):
# add something to axes
# ax.plot(x_vals, y_vals, "bo", linewidth=2, markersize=3, linestyle="solid")

# draw the plot
# plt.draw()
# plt.pause(0.01)
# plt.show()
