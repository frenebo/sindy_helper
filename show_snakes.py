import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from snakeutils.files import extract_snakes

if __name__ == "__main__":
    print("usage: 2 arguments: directory with snake text files, directory to save images")

    dir_name = sys.argv[1]
    image_dir_name = sys.argv[2]
    colorful = len(sys.argv) > 3 and sys.argv[3] == "colorful"
    filenames = os.listdir(dir_name)

    for filename in filenames:
        fp = os.path.join(dir_name,filename)

        with open(fp, "r") as snake_file:
            snakes = extract_snakes(snake_file)
            for snake_idx, snake_pts in enumerate(snakes):
                snake_pts = np.array(snake_pts)

                x,y = snake_pts.T

                if colorful:
                    plt.plot(x,y)
                else:
                    plt.plot(x,y,'b')

            # some_snakefile.tif => some_snakefile.jpg
            save_img_filename = "".join(filename.split(".")[:-1]) + ".png"
            save_img_fp = os.path.join(image_dir_name,save_img_filename)

            plt.axes().set_aspect('equal', adjustable='box')
            # invert y axis
            plt.axis([0,2304,2304,0])
            plt.xlabel("x")
            plt.ylabel("y")
            plt.savefig(save_img_fp)
            # clear figure so we can do the next plot
            plt.clf()

