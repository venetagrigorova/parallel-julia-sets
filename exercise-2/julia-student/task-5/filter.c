/*
 * (C) 2021 Sascha Hunold
 */

#include <math.h>
#include "filter.h"
#include <omp.h>

const int fwidth2  = 1;
const int fheight2 = 1;
void apply_filter(png_bytep *row_pointers, png_bytep *buf, int width, int height, double filter[3][3], int rounds) {
    for (int r = 0; r < rounds; r++) {
        #pragma omp parallel
        {
            #pragma omp single
            {
                for (int i = fwidth2; i < width - fwidth2; i++) {
                    #pragma omp task firstprivate(i)
                    {
                        for (int j = fheight2; j < height - fheight2; j++) {
                            filter_on_pixel(row_pointers, buf, i, j, filter);
                        }
                    }
                }
            }
        }

        // Swap buffer with image
        png_bytep *tmp = buf;
        buf = row_pointers;
        row_pointers = tmp;
    }
}

