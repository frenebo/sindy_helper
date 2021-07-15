import argparse
from snakeutils.files import readable_dir
import os
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import subprocess
import tqdm
from ctypes import c_int32
import time

def run_soax(soax_args,error_dir=None):
    batch_soax = soax_args["batch_soax"]
    tif_dir = soax_args["tif_dir"]
    param_fp = soax_args["param_fp"]
    params_output_dir = soax_args["params_output_dir"]

    if error_dir is not None:
        error_fp = os.path.join(error_dir,params_output_dir + ".txt")
        error_file =  open(error_fp,"w")

    command = "{batch_soax} --image {tif_dir} --parameter {param_fp} --snake {params_output_dir}".format(
        batch_soax = batch_soax,
        tif_dir=tif_dir,
        param_fp=param_fp,
        params_output_dir=params_output_dir,
    )

    print("Executing '{}'".format(command))
    try:
        if error_dir is not None:
            code = subprocess.run(command,shell=True,stderr=error_file,check=True).returncode
        else:
            code = subprocess.run(command,shell=True,check=True).returncode
    except subprocess.CalledProcessError as e:
        print("ERROR: ")
        print("Failed to run {}. return code {}. stderr:".format(e.returncode, command))
        print(e.stderr)
        # print("stdout:")
        # print(e.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try some parameters for snakes')
    parser.add_argument('batch_soax',help="Path to batch_soax executable")
    parser.add_argument('tif_dir',type=readable_dir,help='Directory with tif files to run in soax')
    parser.add_argument('params_dir',type=readable_dir,help='Directory with soax param text files')
    parser.add_argument('output_dir',type=readable_dir,help='Directory to put')
    parser.add_argument('--error_dir',default=None,type=readable_dir,help='Directory to write error messages')
    parser.add_argument('--workers', default=5, type=int, help='Number of batch_soax processes to have running at once')

    args = parser.parse_args()
    param_files = [filename for filename in os.listdir(args.params_dir) if filename.endswith(".txt")]
    param_files.sort()

    workers_num = args.workers
    print("WORKERS: {}".format(workers_num))

    soax_args = []
    for params_filename in param_files:
        param_fp = os.path.join(args.params_dir,params_filename)
        params_name = params_filename[:-len(".txt")]
        params_output_dir = os.path.join(args.output_dir,params_name)

        soax_args.append({
            "batch_soax": args.batch_soax,
            "tif_dir": args.tif_dir,
            "param_fp": param_fp,
            "params_output_dir": params_output_dir,
        })

    print("Creating snake output directories inside {}".format(args.output_dir))
    for soax_arg in soax_args:
        params_output_dir = soax_arg["params_output_dir"]
        os.mkdir(params_output_dir)
        print("Directory '{}' created".format(params_output_dir))

    counter = mp.Value(c_int32)
    counter_lock = mp.Lock()

    with tqdm.tqdm(total=len(soax_args)) as pbar:
        with ThreadPool(workers_num) as pool:
            future = pool.map_async(run_soax, soax_args,args.error_dir)
            while not future.ready():
                if counter.value != 0:
                    with counter_lock:
                        increment = counter.value
                        counter.value = 0
                    pbar.update(n=increment)
                time.sleep(1)
            result = future.get()


