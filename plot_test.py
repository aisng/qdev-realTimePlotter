import random
import matplotlib.pyplot as plt

plt.title("Data")
plt.xlabel("x")
plt.ylabel("y")

x = 0
for i in range(10):
    y = random.randint(0, 10)
    x += random.randint(1, 10)
    plt.plot(x, y, "-", linewidth=2, markersize=3, linestyle="solid")

    plt.pause(1)
plt.show()
