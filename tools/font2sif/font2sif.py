#!/usr/bin/env python3
'''
 * Copyright 2020 Alex Portnov
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

import os
import sys
import math
from struct import *
import argparse
import zlib
import json

#######################################################################
if sys.version_info < (3,0):
    print("Sorry, requires Python 3.x or newer")
    exit(-1)

try:
    import numpy as np
    from PIL import Image
    import freetype
except ImportError:
    print("Please install missing modules: 'pip3 install numpy freetype-py Pillow'")
    exit(-1)
    pass

#######################################################################
def range_parser(s):
    try:
        s, e = map(lambda x:int(x,16), s.split(':'))
        return s, e
    except:
        raise argparse.ArgumentTypeError("Range must be in START:END format")

def char_parser(s):
    try:
        return int(s,16)
    except:
        raise argparse.ArgumentTypeError("Range must be in hex format")

#######################################################################
parser = argparse.ArgumentParser(description='Converting TrueType/OpenType/WOF Fonts to SIF (System Independent Font) format (used by emWin embeded GUI)')
parser.add_argument('--path', type=argparse.FileType('r'), required=True, help='Path to font file')
parser.add_argument('--size', type=int, default=36, help='Pixel font size')
parser.add_argument('--bpp', type=int, choices=[1, 2, 4], default=2, help='Bit per pixel')
parser.add_argument('--ranges', type=range_parser, nargs='*', default=[(0x0020,0x007E)], help='Included character ranges (--ranges 0x0020:0x007E 0x0090:0x0A00)')
parser.add_argument('--exclude', type=char_parser, nargs='*', default=[], help='Exclude character list (--exclude 0x00AA 0x00BB)')
parser.add_argument('--quiet', action='store_false', help='Do not output to std')
parser.add_argument('--norender', action='store_false', help='Do not render preview image')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()
font_path=args.path.name
req_pix_size = args.size
bit_per_pixel=args.bpp
char_ranges=args.ranges
ignore_list=args.exclude
save_render=args.norender
verbose=args.quiet

#######################################################################
face = freetype.Face(font_path)

if verbose:
    print("------------------------------------------")
    print('Num faces   :', face.num_faces)       # number of faces in file
    print('Num glyphs  :', face.num_glyphs)      # number of glyphs in the face
    print('Family name :', face.family_name)     # face family name
    print('Syle name   :', face.style_name)      # face syle name
    print('PS name     :', face.postscript_name) # the postscript name
    print("------------------------------------------")

pix_size=min(200, max(12,req_pix_size))
face.set_char_size(int(pix_size*64), 0, 72, 72)

up_max = -9999
down_min = 9999
total_width = 0
lowercase_y = 0
capital_y = 0
max_width = 0

if len(char_ranges) < 1:
    char_ranges = [(0x0000,0xFFFF)]

# hold per range info
output_data = []

#######################################################################
for r in char_ranges:
    for c in range(r[0], r[1] + 1):
        if c in ignore_list or 0 == face.get_char_index(c):
            continue

        face.load_char(c)
        glyph = face.glyph.get_glyph()
        bitmap = face.glyph.bitmap
        
        left = face.glyph.bitmap_left
        top = face.glyph.bitmap_top
        advance = int(face.glyph.advance.x/64)

        w = max(bitmap.width + left, advance)
        total_width += w
        max_width = max(max_width, w)

        up_max = max(up_max, top)
        down_min = min(down_min, top - bitmap.rows)

        if chr(c) == 'A':
            capital_y = int(top - (top - bitmap.rows))
        if chr(c) == 'a':
            lowercase_y = int(top - (top - bitmap.rows))


max_height = int(up_max - down_min)
baseline = abs(down_min)

if lowercase_y == 0:
    lowercase_y = max_height

if capital_y == 0:
    capital_y = max_height

#######################################################################
if save_render:
    img = np.zeros((max_height,total_width), dtype='ubyte')

# calc binary offsets - all the headers combined
total_headers_size = 16 + 4*len(char_ranges)
for r in char_ranges:
    for c in range(r[0], r[1] + 1):
        total_headers_size += 16

# generate binary data
x = 0
y_base = 0
total_binary_size = 0
for r in char_ranges:
    range_data = []
    for c in range(r[0], r[1] + 1):
        if c in ignore_list or 0 == face.get_char_index(c):
            range_data.append((c, 0, 0, 0, 0, 0, 0, []))
            continue

        face.load_char(c, freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_BITMAP)
        glyph = face.glyph.get_glyph()
        flags = freetype.FT_RENDER_MODE_NORMAL
        if bit_per_pixel < 2:
            flags = freetype.FT_RENDER_MODE_MONO
        bitmap = glyph.to_bitmap(flags, freetype.Vector(0,0), True).bitmap

        left = face.glyph.bitmap_left
        top = face.glyph.bitmap_top
        w,h,pitch = bitmap.width, bitmap.rows, bitmap.pitch
        advance = int(face.glyph.advance.x/64)
        bsize = max(1, math.ceil(h*math.ceil(w*bit_per_pixel/8.0)))

        binData = np.zeros(bsize, dtype='ubyte')
        if w > 0 and h > 0:
            bit_mask = (1 << bit_per_pixel) - 1
            bit_pad = (1 << (8 - bit_per_pixel)) - 1
            arr = np.array(bitmap.buffer, dtype='ubyte')

            # convert tt displayable image in proper pixel depth
            if bit_per_pixel > 1:
                #char_img = arr.reshape(h,w)
                char_img = np.zeros((h,w), dtype='ubyte')
                for yy in range(0, h):
                    for xx in range(0, w):
                        byte = yy*pitch + xx
                        xbit = (arr[byte] >> (8 - bit_per_pixel)) & bit_mask
                        char_img[yy][xx] = (xbit << (8 - bit_per_pixel))
                        # set lsb to keep the display image brightness in grayscale
                        if xbit > 0:
                            char_img[yy][xx] |= bit_pad

            else:
                char_img = np.zeros((h,w), dtype='ubyte')
                for yy in range(0, h):
                    for xx in range(0, w):
                        byte = int(yy*pitch + xx / 8)
                        bit = 7 - (xx % 8)
                        if (arr[byte] & (1 << bit)) != 0:
                            char_img[yy][xx] = 0xFF

            # push binary data
            idx_out = 0
            pixels_per_byte = int(8/bit_per_pixel)
            bit_shift = (8 - bit_per_pixel)
            for yy in range(0, h):
                curr = 0
                curr_cc = 0
                for xx in range(0, w):
                    p = (char_img[yy][xx] >> bit_shift) & bit_mask
                    curr |= (p << (bit_shift - curr_cc))
                    curr_cc += bit_per_pixel
                    if curr_cc >= 8:
                        binData[idx_out] = curr
                        curr_cc = 0
                        curr = 0
                        idx_out+=1

                # line reminder
                if curr_cc > 0:
                    binData[idx_out] = curr
                    curr_cc = 0
                    curr = 0
                    idx_out+=1

            if save_render:
                y = y_base + max(0, max_height - (baseline + top))
                img[y:y+h,x:x+w] = char_img
        else:
            w = 1
            h = 1

        if verbose:
            print("0x{:04X}\t({})\tsize: {}:{}\tshift: {}:{}\tinc: {}\t\t\t{} bytes".format(c, chr(c), w, h, left, top, advance, bsize))

        range_data.append((c, w, h, left, top, advance, total_headers_size + total_binary_size, binData))
        total_binary_size += bsize
        x += advance

    output_data.append(range_data)

if verbose:
    print("------ total font size {} bytes ------ ".format(total_binary_size + total_headers_size))

#######################################################################
out_file_path = font_path + "." + str(max_height) + "x" + str(max_width)+ "." + str(bit_per_pixel) + "bpp"
if save_render:
    img = Image.fromarray(img)
    img.save(out_file_path + ".png")

#######################################################################
jsonFile = open(out_file_path + ".json", "w")
fontsXDict = {}
# write header
binfile = open(out_file_path + ".sif", "wb")

# SIF format (all values LSB): GUI_SI_FONT
binfile.write(pack("BBBB", 0x47, 0x55, 0x49, 0x50))     # U32 Bytes ID (0x47, 0x55, 0x49, 0x50, "GUIP")
binfile.write(pack("<H", max_height))                   # U16 ySize of font /* height of font  */
binfile.write(pack("<H", max_height))                   # U16 yDist of font, to be used for cursor increment  /* space of font y */
binfile.write(pack("<H", (max_height - baseline)))      # U16 Baseline position from top  /* Baseline */
binfile.write(pack("<H", lowercase_y))                  # U16 Height in pixels of lowercase characters     /* Height of lowercase characters */
binfile.write(pack("<H", capital_y))                    # U16 Height in pixels of capital characters  /* Height of capital characters */
binfile.write(pack("<H", len(char_ranges)))             # U16 - number of ranges

#  write range data
# GUI_SIF_CHAR_AREA -- all ranges back to back
for r in char_ranges:
    binfile.write(pack("<H", r[0]))     # U16 First codepoint in access table /* first character */
    binfile.write(pack("<H", r[1]))     # U16 Last codepoint in access table  /* last character  */

# GUI_SIF_CHARINFO_EXT - Character Access table (for all in range of "last character" - "first character")
# write char info data data
for i in range(0, len(char_ranges)):
    r = char_ranges[i]
    d = output_data[i]
    for i in range(0, r[1] - r[0] + 1):
        c, w, h, left, top, advance, binary_offset, data = d[i]
        binfile.write(pack("<H", w))                                # U16 X-size of bitmap
        binfile.write(pack("<H", h))                                # U16 Y-size of bitmap
        binfile.write(pack("<h", left))                             # I16 X-position of bitmap
        binfile.write(pack("<h", max_height - (baseline + top)))    # I16 Y-position of bitmap
        binfile.write(pack("<H", advance))                          # U16 X-distance in pixels to be used for cursor increment
        binfile.write(pack("<H", 0))                                # U16 dummy - 00
        binfile.write(pack("<I", binary_offset))                    # U32 Position of bitmap information in file (0 means character is not available)
        fontsXDict[c]=advance

# write binay data
for i in range(0, len(char_ranges)):
    for c, _, _, _, _, _, _, data in output_data[i]:
        if len(data) > 0:
            binfile.write(data.tobytes())

binfile.close()
jsonFile.write(json.dumps({"max_height":max_height,"char_width":fontsXDict}))
jsonFile.close()
# compress to zlib
fd = open(out_file_path + ".sif", "rb")
bindata = fd.read()
fd.close()
fd = open(out_file_path + ".sifz", "wb")
fd.write(zlib.compress(bindata, 9))
fd.close()
