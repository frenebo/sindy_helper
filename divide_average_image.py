
from snakeutils.logger import PrintLogger
import os
import numpy as np
from PIL import Image
from snakeutils.files import has_one_of_extensions
from snakeutils.tifimage import save_3d_tif, pil_img_3d_to_np_arr
from multiprocessing.pool import ThreadPool

def divide_average_image(source_dir, target_dir, logger=PrintLogger):
    source_tifs = [filename for filename in os.listdir(source_dir) if has_one_of_extensions(filename, [".tif", ".tiff"])]
    source_tifs.sort()

    if len(source_tifs) == 0:
        logger.error("No .tif files found in {}".format(source_dir))
        return


    if len(source_tifs) < 20:
        logger.log("Warning: less than 20 source tifs. Dividing image average works best for large data sets.")


    first_pil_img = Image.open(os.path.join(source_dir, source_tifs[0]))
    first_tiff_arr = pil_img_3d_to_np_arr(first_pil_img)
    img_shape = first_tiff_arr.shape

    sum_image = np.zeros(img_shape, dtype=np.double)

    # image_count = 0
    for tiff_name in source_tifs:
        pil_img = Image.open(os.path.join(source_dir, tiff_name))
        np_arr = pil_img_3d_to_np_arr(pil_img)
        sum_image += np_arr

    average_image = (sum_image / len(source_tifs))
    # average_image /= average_image.max()
    image_mult_factor = np.reciprocal(average_image)
    image_mult_factor /= image_mult_factor.max()
    logger.log("Biggest division factor (inverse): {}".format(image_mult_factor.min()))
    # print()
    # avg_reciprocal /= avg_reciprocal.

    # avg_max_bright = average_image.max()
    # mult_factors = average_image / avg_max_bright

    for tiff_name in source_tifs:
        pil_img = Image.open(os.path.join(source_dir, tiff_name))
        np_arr = pil_img_3d_to_np_arr(pil_img)
        # original_dtype = np_arr.dtype
        divided_arr = np.multiply(np_arr.astype(np.double), image_mult_factor)
        divided_arr = divided_arr.astype(np_arr.dtype)
        # print(divided_arr.dtype)
        # where_less_than_average = np_arr < average_image
        # np_arr = np_arr - average_image
        # np_arr[where_less_than_average] = 0
        save_tiff_fn = "avg_divided_" + tiff_name
        save_tiff_path = os.path.join(target_dir, save_tiff_fn)
        save_3d_tif(save_tiff_path, np_arr)