import json
import argparse

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON snake viewer')
    parser.add_argument("json_path")

    args = parser.parse_args()

    with open(args.json_path, "r") as f:
        snakes = json.load(f)

    fig = plt.figure()
    ax = plt.axes(projection="3d")

    for snake_info in snakes:
        x = []
        y = []
        z = []
        for snake_pt in snake_info:
            pt_x,pt_y,pt_z = snake_pt["pos"]
            x.append(pt_x)
            y.append(pt_y)
            z.append(pt_z)
        ax.plot(x,y,z)


    plt.show()