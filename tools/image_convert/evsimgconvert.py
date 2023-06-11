#!/usr/bin/env python3
'''
 * Copyright 2022 Everysight LTD
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x or newer")
    exit(-1)


__version_info__ = ('1', '0', '1')
__version__ = '.'.join(__version_info__)

try:
    from PIL import __version__ as PIL_VERSION
    from PIL import Image
    from PIL.PngImagePlugin import PngImageFile, PngInfo
except ImportError:
    print("Please install missing modules: 'pip3 install Pillow'")
    exit(-1)


pil_old = True
try:
    pil_min_version = [8,1,0]
    pil_cur_version = [int(x) for x in PIL_VERSION.split('.')]
    pil_old = pil_min_version[0] > pil_cur_version[0] or (pil_min_version[0] == pil_cur_version[0] and pil_min_version[1] > pil_cur_version[1])
except:
    pass
if pil_old:
    print("You have an unsupported Pillow version {}".format(PIL_VERSION))
    print("You need to have Pillow version '8.1.0' or greater, please upgrade with 'pip3 install Pillow -U'")
    exit(-1)

#############################################################################################
import os
import argparse
from time import perf_counter
import subprocess as sp
import tempfile
import shutil
import logging


MIN_OPTIPNG_PCT = 0.1
MAX_SIZE = 16*1024

#############################################################################################
class Message:
    def __init__(self, fmt, args):
        self.fmt = fmt
        self.args = args

    def __str__(self):
        return self.fmt.format(*self.args)


class StyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(StyleAdapter, self).__init__(logger, extra or {})

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, Message(msg, args), (), **kwargs)


logger = StyleAdapter(logging.getLogger("epsimgconvert"))

#############################################################################################
M332_color3bit = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,
    0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,
    0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
    0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
    0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x05,
    0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
    0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
    0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
    0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
    0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x07, 0x07, 0x07,
    0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07
]

# b = (b + 42) / 85;
M332_color2bit = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
    0x02, 0x02, 0x02, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,
    0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,
    0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03
]

# b = x * 85;
M332_2bitColor = [0x00, 0x55, 0xaa, 0xff]

# g = (x & 7) * 255 / 7;
M332_3bitColor = [0x00, 0x24, 0x48, 0x6d, 0x91, 0xb6, 0xda, 0xff]

#############################################################################################
def color2index_m332(color):
    b = color & 255
    g = (color >> 8) & 255
    r = (color >> 16) & 255
    return M332_color2bit[b] | (M332_color3bit[g] << 2) | (M332_color3bit[r] << 5)


def rgb2index_m332(color):
    r = color[0] & 255
    g = color[1] & 255
    b = color[2] & 255
    return M332_color2bit[b] | (M332_color3bit[g] << 2) | (M332_color3bit[r] << 5)


def index2color_m332(index):
    b = M332_2bitColor[(index & 3)]
    g = M332_3bitColor[(index >> 2) & 0x7]
    r = M332_3bitColor[(index >> 5) & 0x7]
    return [r, g, b, 255]

#############################################################################################
def is_eeps_chunk_present(img: PngImageFile):
    for chunk in img.private_chunks:
        if chunk[0] == b'eePS':
            return True

    return False

#############################################################################################
def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

#############################################################################################
def get_image_magick_convert_tool(tool):
    cmd = which(tool)
    if cmd is None:
        return None
    result = sp.run([cmd, "--version"], stdout=sp.PIPE)
    if result.returncode != 0:
        return None
    output = result.stdout.decode("utf-8")
    if "ImageMagick" in output:
        return cmd
    return None

#############################################################################################
def get_optipng_tool(tool):
    cmd = which(tool)
    if cmd is None:
        return None
    result = sp.run([cmd, "--version"], stdout=sp.PIPE)
    if result.returncode != 0:
        return None
    output = result.stdout.decode("utf-8")
    if "OptiPNG" in output:
        return cmd
    return None

#############################################################################################
def convert(fn, out_fn, keep_alpha):
    img = Image.open(fn)
    if type(img) == PngImageFile and is_eeps_chunk_present(img):
        logger.warning("This image already appears to be optimized.")
        return None

    save_alpha = 'A' in img.mode and keep_alpha
    logger.debug("Image mode: {}, keep_alpha:{}", img.mode, keep_alpha)
    if img.mode == 'L' or img.mode == 'LA' or img.mode == '1' or img.mode == 'P':
        if save_alpha == False:
            img = img.convert("RGB")
        else:
             img = img.convert("RGBA")

    data = img.getdata()
    newData = [0]*(img.width*img.height)
    for i, el in enumerate(data):
        if save_alpha:
            newData[i] = (rgb2index_m332(el), el[3])
        else:
            if img.mode != 'RGB':
                f = float(el[3])/255.0
                newel = (int(el[0]*f),int(el[1]*f),int(el[2]*f))
                newData[i] = rgb2index_m332(newel)
            else:
                newData[i] = rgb2index_m332(el)

        logger.debug("{}:{} => {}", i, el, newData[i])

    info = PngInfo()
    info.add(b'eePS', b'')

    newMode = 'L'
    if save_alpha:
        newMode = 'LA'
    newImg = Image.new(newMode, (img.width, img.height))
    newImg.putdata(newData)
    newImg.save(out_fn, pnginfo=info, optimize=True)
    return True

#############################################################################################
def view(fn):
    img = Image.open(fn)

    decodeEps = type(img) == PngImageFile and is_eeps_chunk_present(img)
    data = img.getdata()
    logger.debug('Mode:', img.mode)
    inBytesPerPixel = 1
    if img.mode == 'P':
        img = img.convert('LA')
        logging.debug('converted, new mode:', img.mode)
        data = img.getdata()
    if decodeEps and (img.mode == 'L' or img.mode == 'LA'):
        if img.mode == 'LA':
            inBytesPerPixel = 2

        start = perf_counter()
        newData = [0]*(img.width*img.height*4)
        for i, el in enumerate(data):
            index = el
            if inBytesPerPixel == 2:
                index = el[0]
            c = index2color_m332(index)
            newData[i*4:i*4+4] = c
        delta = perf_counter() - start
        logging.debug("Fix took: {}".format(delta))

        try:
            import matplotlib.pyplot as plt
            import numpy as np
            newData = np.array(newData, int)
            plt.imshow(newData.reshape((img.height, img.width, 4)))
            plt.show()
        except ImportError:
            logger.error(
                "Missing modules: matplotlib, numpy, please install with: 'pip3 install numpy matplotlib'")
    else:
        img.show("Hello")

#############################################################################################
def convert_to_png(convert, src, dst):
    result = sp.run([convert, src, dst], stdout=sp.PIPE)
    if result.returncode != 0:
        logger.warning("Unable to convert image:")
        logger.warning(result.stdout.decode("utf-8"))

    return result.returncode == 0

#############################################################################################
def optipng(optipng, image):
    with tempfile.TemporaryDirectory() as tmp:
        outfn = os.path.join(tmp, "out.png")
        result = sp.run([optipng, "-quiet", "-o7", "-f3",
                         image, "-out", outfn], stdout=sp.PIPE)
        if result.returncode != 0:
            logger.warning("Unable to optimize image:")
            logger.warning(result.stdout.decode("utf-8"))
        in_size = os.stat(image).st_size
        out_size = os.stat(outfn).st_size
        pct = ((in_size - out_size) / in_size)
        if pct > MIN_OPTIPNG_PCT:
            shutil.copyfile(outfn, image)
        else:
            logger.warning(
                "Ignoring optipng output, result was not optimal:{:.2f} %", pct)

    return result.returncode == 0

#############################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Everysight Epsilon Image Converter / Viewer')
    parser.add_argument('-s', '--show', action='store_true', default=False, help='Show image')
    parser.add_argument('-c', '--convert', action='store_true', default=True, help='Convert image')
    parser.add_argument('image', type=str, help='Image file')
    parser.add_argument('-v', '--verbose',action='store_true', help='Be Verbose')
    parser.add_argument('-a', '--alpha', action='store_true',help='keep Alpha channel')
    parser.add_argument('-o', "--out", type=str, help="Output file name",default="out.png", required=False)
    parser.add_argument("--imageMagick", type=str, help="Path to ImageMagick convert tool", default="convert", required=False)
    parser.add_argument("--optipng", type=str, help="Path to optipng tool", default="optipng", required=False)
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()
    log_level = logging.WARNING
    if args.verbose:
        log_level = logging.DEBUG

    FORMAT = '%(message)s'

    logging.basicConfig(format=FORMAT)
    logger.setLevel(log_level)

    img_convert_cmd = get_image_magick_convert_tool(args.imageMagick)
    optipng_cmd = get_optipng_tool(args.optipng)

    logger.debug("Using ImageMagick convert:{}", img_convert_cmd)

    if os.path.isfile(args.image) is False:
        logger.error("Not a file: {}", args.image)
        sys.exit(-1)

    isSVG = os.path.splitext(args.image)[-1].lower() == '.svg'

    outFnIsPng = args.out.lower().endswith('.png')
    if not outFnIsPng:
        logger.error("This tool converts images to PNG file format!\nYou requested output filename to be:{}",args.out)
        logger.error("output filename must end in .png")
        sys.exit(-1)

    if args.show:
        if isSVG:
            logger.warning("Unabel to preview SVG images, sorry :(")
            sys.exit(-1)
        view(args.image)
    elif args.convert:
        in_size = os.stat(args.image).st_size
        if isSVG:
            if img_convert_cmd is None:
                logger.error(
                    "Input image is an SVG file, and ImageMagic is not found in PATH")
                logger.error(
                    "If ImageMagick is installed, consider running with: --imageMagic PATH_TO_IMAGEMAGIC_CONVERT_BINARY")
                logger.error(
                    "i.e: --imageMagic /opt/imageMagic-6.19/bin/convert")
                logger.error("See: https://imagemagick.org/")
                sys.exit(1)
            if convert_to_png(img_convert_cmd, args.image, args.out) is False:
                sys.exit(1)
            args.image = args.out

        ret = False
        ret = convert(args.image, args.out, args.alpha)
        if(ret is None):
            pass
        elif ret and optipng_cmd is not None:
            ret = optipng(optipng_cmd, args.out)
        else:
            logger.warning("No optipng tool found, output PNG is not optimal")
            logger.warning(
                "If optipng is installed, consider running with: --optipng PATH_TO_OPTIPNG_BINARY")
            logger.warning("i.e: --optipng /opt/optipng/bin/optipng")
            logger.warning("See: http://optipng.sourceforge.net/")

        exitCode = 0
        if ret is False or ret is None:
            exitCode = 1
        else:
            out_size = os.stat(args.out).st_size
            src_is_better = in_size < out_size and isSVG is False and in_size < MAX_SIZE
            if src_is_better:
                logger.error(
                    "It appears that you better use the source image:{}", args.image)
                exitCode = 1
            elif out_size >= MAX_SIZE:
                logger.error(
                    "Image is too large! Size after optimization:{} bytes, try smaller image.", out_size)
                exitCode = 1
            else:
                logger.warning("Source size:{}, Output size: {} bytes = {:.2f}% decrese",
                               in_size, out_size, ((in_size-out_size)/in_size)*100)

        sys.exit(exitCode)
