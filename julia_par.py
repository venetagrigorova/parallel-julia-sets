#! /usr/bin/env python

from re import U
import numpy as np
import argparse
import time
from multiprocessing import Pool, TimeoutError
from julia_curve import c_from_group

# Update according to your group size and number (see TUWEL)
GROUP_SIZE   = 3
GROUP_NUMBER = 3

# do not modify BENCHMARK_C
BENCHMARK_C = complex(-0.2, -0.65)

def compute_julia_set_sequential(xmin, xmax, ymin, ymax, im_width, im_height, c):

    zabs_max = 10
    nit_max = 300

    xwidth  = xmax - xmin
    yheight = ymax - ymin

    julia = np.zeros((im_width, im_height))
    for ix in range(im_width):
        for iy in range(im_height):
            nit = 0
            # Map pixel position to a point in the complex plane
            z = complex(ix / im_width * xwidth + xmin,
                        iy / im_height * yheight + ymin)
            # Do the iterations
            while abs(z) <= zabs_max and nit < nit_max:
                z = z**2 + c
                nit += 1
            ratio = nit / nit_max
            julia[ix,iy] = ratio

    return julia

def compute_patch(task):
    # x_start, y_start: top-left corner of this patch in the full image
    # patch: patch size in pixels (width = height)
    # meta: tuple with shared values like image size and complex plane bounds
    x_start, y_start, patch, meta = task
    size, xmin, xmax, ymin, ymax, c = meta

    # create an empty patch image to store computed values
    patch_img = np.zeros((patch, patch))

    # calculate pixel-to-complex-plane scaling
    xwidth = xmax - xmin
    yheight = ymax - ymin

    zabs_max = 10 # maximum absolute value of z
    nit_max = 300 # maximum number of iterations

    for ix in range(patch):
        for iy in range(patch):
            nit = 0
            px = x_start + ix
            py = y_start + iy

            # skip corners if patch extends outside image bounds
            if px >= size or py >= size:
                continue

            # map pixel position to complex plane
            z = complex(px / size * xwidth + xmin,
                        py / size * yheight + ymin)

            # do the iterations
            while abs(z) <= zabs_max and nit < nit_max:
                z = z**2 + c
                nit += 1

            # compute the ratio of iterations to max iterations
            # and store it in the patch image (used for colouring)
            ratio = nit / nit_max
            patch_img[ix, iy] = ratio

    return (x_start, y_start, patch_img)

def compute_julia_in_parallel(size, xmin, xmax, ymin, ymax, patch, nprocs, c):
    # prepare metadata that is shared across the patches
    meta = (size, xmin, xmax, ymin, ymax, c)
    tasks = []

    # divide the full image into patches
    # each task is a patch starting at (x, y) and going to (x+patch, y+patch)
    for x in range(0, size, patch):
        for y in range(0, size, patch):
            tasks.append((x, y, patch, meta))

    # compute in parallel
    with Pool(processes=nprocs) as pool:
        completed = pool.map(compute_patch, tasks, chunksize=1)

    # assemble the final image
    julia_img = np.zeros((size, size))
    for x_start, y_start, patch_img in completed:
        x_end = min(x_start + patch_img.shape[0], size)
        y_end = min(y_start + patch_img.shape[1], size)
        julia_img[x_start:x_end, y_start:y_end] = patch_img[:x_end - x_start, :y_end - y_start]

    return julia_img


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="image size in pixels (square images)", type=int, default=500)
    parser.add_argument("--xmin", help="", type=float, default=-1.5)
    parser.add_argument("--xmax", help="", type=float, default=1.5)
    parser.add_argument("--ymin", help="", type=float, default=-1.5)
    parser.add_argument("--ymax", help="", type=float, default=1.5)
    parser.add_argument("--group-size", help="", type=int, default=None)
    parser.add_argument("--group-number", help="", type=int, default=None)
    parser.add_argument("--patch", help="patch size in pixels (square images)", type=int, default=20)
    parser.add_argument("--nprocs", help="number of workers", type=int, default=1)
    parser.add_argument("--draw-axes", help="Whether to draw axes", action="store_true")
    parser.add_argument("-o", help="output file")
    parser.add_argument("--benchmark", help="Whether to execute the script with the benchmark Julia set", action="store_true")
    args = parser.parse_args()

    #print(args)
    if args.group_size is not None:
        GROUP_SIZE = args.group_size
    if args.group_number is not None:
        GROUP_NUMBER = args.group_number

    # assign c based on mode
    c = None
    if args.benchmark:
        c = BENCHMARK_C 
    else:
        c = c_from_group(GROUP_SIZE, GROUP_NUMBER) 

    stime = time.perf_counter()
    julia_img = compute_julia_in_parallel(
        args.size,
        args.xmin, args.xmax, 
        args.ymin, args.ymax, 
        args.patch,
        args.nprocs,
        c)
    rtime = time.perf_counter() - stime

    print(f"{args.size};{args.patch};{args.nprocs};{rtime}")

    if not args.o is None:
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        fig, ax = plt.subplots()
        ax.imshow(julia_img, interpolation='nearest', cmap=plt.get_cmap("hot"))

        if args.draw_axes:
            # set labels correctly
            im_width = args.size
            im_height = args.size
            xmin = args.xmin
            xmax = args.xmax
            xwidth = args.xmax - args.xmin
            ymin = args.ymin
            ymax = args.ymax
            yheight = args.ymax - args.ymin

            xtick_labels = np.linspace(xmin, xmax, 7)
            ax.set_xticks([(x-xmin) / xwidth * im_width for x in xtick_labels])
            ax.set_xticklabels(['{:.1f}'.format(xtick) for xtick in xtick_labels])
            ytick_labels = np.linspace(ymin, ymax, 7)
            ax.set_yticks([(y-ymin) / yheight * im_height for y in ytick_labels])
            ax.set_yticklabels(['{:.1f}'.format(-ytick) for ytick in ytick_labels])
            ax.set_xlabel("Imag")
            ax.set_ylabel("Real")
        else:
            # disable axes
            ax.axis("off") 

        plt.tight_layout()
        plt.savefig(args.o, bbox_inches='tight')
        #plt.show()