#include <stdio.h>
#include <complex.h>
#include <omp.h>

#include "juliap.h"

void compute_julia_set(double xmin, double xmax, double ymin, double ymax, 
    double **image, int im_width, int im_height)
{
    double zabs_max = 10;
    double complex c = -0.1 + 0.65 * I;
    int nit_max = 1000;

    double xwidth  = xmax - xmin;
    double yheight = ymax - ymin;

    // parallelize the two loops with openmp
    #pragma omp parallel for collapse(2) schedule(runtime)
    for(int i = 0; i < im_width; i++) {
        for(int j = 0; j < im_height; j++) {
            int nit = 0;
            double complex z;

            // map pixel (i,j) to complex plane
            z = (double)i / (double)im_width * xwidth + xmin 
              + ((double)j / (double)im_height * yheight + ymin) * I;

            // iterate z = z^2 + c
            while( cabs(z) <= zabs_max && nit < nit_max ) {
                z = cpow(z, 2) + c;
                nit += 1;
            }

            // store normalized iteration count
            image[i][j] = (double)nit / (double)nit_max;
        }
    }
}
