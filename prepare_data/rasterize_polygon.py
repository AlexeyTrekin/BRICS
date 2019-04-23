import os
import io
import sys
import geojson
import rasterio
from aeronet.dataset import FeatureCollection, rasterize

def clean_markup(filename):
    with io.open(filename, encoding='utf-8') as src:
        data = geojson.loads(src.read())
    feats = []
    for feat in data.features:
         feats.append(geojson.Feature(geometry=feat.geometry, properties={}))
    if hasattr(data, 'crs'):
        crs = data.crs
    else:
        crs = 'EPSG:4326'
    new_fc = geojson.FeatureCollection(crs=crs, features=feats)
    with open(filename, 'w') as dst:
        dst.write(geojson.dumps(new_fc))   

image_name = sys.argv[1]
markup_name = sys.argv[2]

# Getting rid of non-ascii characters in properties (and all the properties whatsoever)
clean_markup(markup_name)

with rasterio.open(image_name) as src:
    tr = src.transform
    shape = [src.height, src.width]
    crs = src.crs

dir = os.path.dirname(os.path.abspath(image_name))
fc = FeatureCollection.read(markup_name).reproject(crs)
rasterize(fc, tr, shape).save(dir)
