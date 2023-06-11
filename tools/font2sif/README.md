
# font2sif
This tinny Python utility converting TrueType/OpenType/WOF Fonts to SIF (System Independent Font) format (namely used by emWin embedded GUI and a like).
The utility supports bit depth (1,2,4bpp), range selection and PNG rendering of preview image of all included characters.

## Why?
Most embedded devices do not support vector-based fonts.
Those has to be rendered in advance to pixel format.
Guess what? Tools to do that are not freely provided with embedded libraries.

## Example

```sh
python3 font2sif.py --help
```

```sh
python3 font2sif.py --path Saira-Regular.ttf --size 36 --bpp 2
```
You can pick character ranges to include, or characters to exclude, reducing the size
```sh
python3 font2sif.py --path Saira-Regular.ttf --size 36 --ranges 0x0020:0x007E 0x0090:0x0A00 --exclude 0x00AA 0x00BB
```

## Script output

Per execution, the script generate 4 files:

- **[Font Name].[HxW].[X]bpp.sifz**: Compressed sif file. **Should be added to the application resoruces**
- **[Font Name].[HxW].[X]bpp.json**: Metadata json file. **Should be added to the application resoruces**
- **[Font Name].[HxW].[X]bpp.sif**: Uncompressed sif file (Should be igonpred whe n using firmware version above 100)
- **[Font Name].[HxW].[X]bpp.png**: Fonts image file. Visual representation for developer validation (Should not be used within the app)

### Example

When running ``py font2sif.py --size 43 --path ./Saira-Regular.ttf --ranges 0x0020:0x007E 0x00E0:0x00FF 0x00BC:0x00E``

We receive the following files:

- **Saira-Regular.ttf.43x43.2bpp.sifz** (Should be added to the application resoruces)
- **Saira-Regular.ttf.43x43.2bpp.json** (Should be added to the application resoruces)
- **Saira-Regular.ttf.43x43.2bpp.sif**
- **Saira-Regular.ttf.43x43.2bpp.png**



## Thanks
Thank to guys from https://www.freetype.org/ they provide the actual rendering engine, making it all possible.
