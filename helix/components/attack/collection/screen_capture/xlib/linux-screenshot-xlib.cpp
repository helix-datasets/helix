#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <CImg.h>
#include <cstdint>
#include <cstring>
#include <vector>

using namespace cimg_library;

void ${linux_screenshot_xlib}(int argc, char*argv[])
{
    // https://stackoverflow.com/questions/8249669/how-do-take-a-screenshot-correctly-with-xlib

    int Width;
    int Height;

    Display* display = XOpenDisplay(nullptr);
    Window root = DefaultRootWindow(display);

    XWindowAttributes attributes = {0};
    XGetWindowAttributes(display, root, &attributes);

    Width = attributes.width;
    Height = attributes.height;

    XImage* img = XGetImage(display, root, 0, 0 , Width, Height, AllPlanes, ZPixmap);

    unsigned char *array = new unsigned char[Width * Height * 3];

    unsigned long red_mask = img->red_mask;
    unsigned long green_mask = img->green_mask;
    unsigned long blue_mask = img->blue_mask;

    CImg<unsigned char> screenshot(array, Width, Height, 1, 3);

    for(int x = 0; x < Width; x++) {
        for(int y = 0; y < Height; y++) {
            unsigned long pixel = XGetPixel(img, x, y);

            unsigned char blue = pixel & blue_mask;
            unsigned char green = (pixel & green_mask) >> 8;
            unsigned char red = (pixel & red_mask) >> 16;

            screenshot(x, y, 0) = red;
            screenshot(x, y, 1) = green;
            screenshot(x, y, 2) = blue;
        }
    }

    screenshot.save_png(${output});

    XDestroyImage(img);
    XCloseDisplay(display);
}
