import argparse
import math
from snakeutils.files import readable_dir
from snakeutils.tifimage import save_3d_tif
import os
import numpy as np
from PIL import Image

def section_tif(tif_filepath,sectioned_dir,section_max_size):
    print("Processing {}".fomat(tif_filepath))

    pil_img = Image.open(fp)

    # If TIF is not 3D
    if getattr(pil_img, "n_frames", 1) == 1:
        raise Exception("TIF {} is not 3D tif".format(tif_filepath))

    width = pil_img.width
    height = pil_img.height
    depth = pil_img.n_frames

    img_arr = np.zeros((height,width,depth,dtype=np.array(pil_img).dtype))
    for i in range(pil_img.n_frams):
        pil_img.seek(i)
        img_arr[:,:,i] = np.array(img_arr)

    # Ceil because we want to have slices on the smaller size if width/height/depth is not
    # exactly divisible by section_size
    width_slices = math.ceil(width / section_max_size)
    height_slices = math.ceil(height / section_max_size)
    depth_slices = math.ceil(depth / section_max_size)

    section_width = math.floor(width / width_slices)
    section_height = math.floor(height / height_slices)
    section_depth = math.floor(depth / depth_slices)

    width_boundaries = [i*section_width for i in range(width_slices)] + [width]
    height_boundaries = [i*section_height for i in range(height_slices)] + [height]
    depth_boundaries = [i*section_depth for i in range(depth_slices)] + [depth]


    for width_idx in range(width_slices):
        for height_idx in range(height_slices):
            for depth_idx in range(depth_slices):
                section_arr = img_arr[
                    width_boundaries[width_idx]:width_boundaries[width_idx + 1],
                    height_boundaries[height_idx]:height_boundaries[height_idx + 1],
                    depth_boundaries[depth_idx]:depth_boundaries[depth_idx + 1],
                ]
                section_filepath = os.path.join(
                    sectioned_dir,
                    "sec_{}_{}_{}".format(height_idx,width_idx,depth_idx),
                )

                save_3d_tif(section_filepath,section_arr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try some parameters for snakes')
    parser.add_argument('section_max_size',type=int,help="Maximum width/height/depth of a sextion (pixels along)")
    parser.add_argument('source_dir',type=readable_dir,help="Directory where source tif files are")
    parser.add_argument('target_dir',type=readable_dir,help="Directory to save secitoned tifs")

    args = parser.parse_args()

    if section_max_size <= 0:
        raise Exception("Section max size must be positive. Invalid value {}".format(args.section_size))

    source_tifs = [filename for filename in os.listdir(args.source_dir) if filename.endswith(".tif")]

    for tif_fn in source_tifs:
        tif_fp = os.path.join(args.source_dir,tif_fn)

        # remove .tif from file name
        image_name_extensionless = fp[:-4]

        sectioned_dir = os.path.join(args.target_dir, "sectioned_" + image_name_extensionless)

        if os.path.exists(sectioned_dir):
            raise Exception("Directory {} already exists".format(sectioned_dir))

        os.mkdir(sectioned_dir)

        section_tif(tif_fp,sectioned_dir,args.section_max_size)
