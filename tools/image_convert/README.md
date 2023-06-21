# Everysight Maverick Image Converter Tool

`evsimgconvert.py` can be used to optimize images (Reduce disk size, improve rendering time).

`evsimgconvert.py` Performs all the work required to optimize the image for Everysight Maverick.
1. Convert image to PNG with 1 Byte color format: 332
2. Attempt to run `optipng` on the output, to further optimize the resulting PNG file.

Sometimes, JPEG compressing is better, especially for photo-realistic images.
This tool will detect this case, and inform you, if you should stick with original image.


## Requirements

1. [Python 3.8.6+](https://www.python.org/)
    a. Python module: Pillow, version: 8.1.0
        
        pip3 install Pillow==8.1.0
2. [OptiPng (PNG optimizer)](http://optipng.sourceforge.net/)

for mac:  brew install optipng
## Optional

[ImageMagick (To convert SVG Images)](https://imagemagick.org/index.php)

for mac: brew install imagemagick

## Usage

```bash
python3 evsimgconvert.py -c source_image.jpeg -o output_image.png
```
By default `alpha` channel will be discarded, if you want to keep it, pass: --alpha:
```bash
python3 evsimgconvert.py --alpha -c source_image.jpeg -o output_image.png
```


## Optional
`evsimgconvert.py` can be used to show the resulting image on screen.
For that to work you need to have two additional Python modules installed:

```bash
pip install numpy matplotlib
```

In order to show the resulting image:
```bash
python3 evsimgconvert.py --show output_image.png
```
