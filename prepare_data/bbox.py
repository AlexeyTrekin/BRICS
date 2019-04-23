import sys
import rasterio
from rasterio.warp import transform


# reading geo attribuites from geotiff image
with rasterio.open(sys.argv[1]) as src:
    tr = src.transform
    h = src.height
    w = src.width
    crs = src.crs

# extract image boundaries
xs = [tr[2], tr[2] + tr[0]*w]
ys = [tr[5], tr[5] + tr[4]*h]

# transform boundaries to the lat|lon coordinate system
xs, ys = transform(crs, 'EPSG:4326', xs, ys)
xs.sort()
ys.sort()

print(str([ys[0], xs[0], ys[1], xs[1]])[1:-1])