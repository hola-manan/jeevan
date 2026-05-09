/*
 * Basic libpng functional test.
 *
 * This test verifies that libpng can be linked and used for a minimal
 * write workflow. It creates a 1x1 RGB PNG image, writes it to disk,
 * reopens the file, and checks the PNG signature to confirm that the
 * output is a valid PNG file.
 */

#include <stdio.h>
#include <stdlib.h>
#include <png.h>

int main(void) {
    const char *filename = "test.png";
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        fprintf(stderr, "failed to open %s for writing\n", filename);
        return 1;
    }

    png_structp png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png_ptr) {
        fprintf(stderr, "png_create_write_struct failed\n");
        fclose(fp);
        return 1;
    }

    png_infop info_ptr = png_create_info_struct(png_ptr);
    if (!info_ptr) {
        fprintf(stderr, "png_create_info_struct failed\n");
        png_destroy_write_struct(&png_ptr, NULL);
        fclose(fp);
        return 1;
    }

    if (setjmp(png_jmpbuf(png_ptr))) {
        fprintf(stderr, "libpng write error\n");
        png_destroy_write_struct(&png_ptr, &info_ptr);
        fclose(fp);
        remove(filename);
        return 1;
    }

    png_init_io(png_ptr, fp);

    png_set_IHDR(
        png_ptr,
        info_ptr,
        1,
        1,
        8,
        PNG_COLOR_TYPE_RGB,
        PNG_INTERLACE_NONE,
        PNG_COMPRESSION_TYPE_BASE,
        PNG_FILTER_TYPE_BASE
    );

    png_write_info(png_ptr, info_ptr);

    png_byte row[3] = {255, 0, 0};
    png_write_row(png_ptr, row);
    png_write_end(png_ptr, NULL);

    png_destroy_write_struct(&png_ptr, &info_ptr);
    fclose(fp);

    fp = fopen(filename, "rb");
    if (!fp) {
        fprintf(stderr, "failed to reopen %s\n", filename);
        return 1;
    }

    unsigned char sig[8];
    if (fread(sig, 1, sizeof(sig), fp) != sizeof(sig)) {
        fprintf(stderr, "failed to read PNG signature\n");
        fclose(fp);
        return 1;
    }
    fclose(fp);

    if (png_sig_cmp(sig, 0, sizeof(sig)) != 0) {
        fprintf(stderr, "output file is not a valid PNG\n");
        return 1;
    }

    printf("libpng OK: wrote valid 1x1 PNG to %s\n", filename);
    return 0;
}
