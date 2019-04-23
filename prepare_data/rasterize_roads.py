import os
import io
import sys
import shapely
import geojson
import rasterio
from aeronet.dataset import Feature, FeatureCollection, rasterize

def clean_markup_road(filename):
    with io.open(filename, encoding='utf-8') as src:
        data = geojson.loads(src.read())
    feats = []
    for feat in data.features:
         feats.append(geojson.Feature(geometry=feat.geometry, 
                                      properties={'highway':feat.properties['highway']}))
    if hasattr(data, 'crs'):
        crs = data.crs
    else:
        crs = 'EPSG:4326'
    new_fc = geojson.FeatureCollection(crs=crs, features=feats)
    with open(filename, 'w') as dst:
        dst.write(geojson.dumps(new_fc))   

def make_poly(road_geometry):
    #if road_feature.properties['highway'] == 'motorway':
    #    width = 20
    #elif road_feature.properties['highway'] == 'trunk':
    #    width = 10
    #elif road_feature.properties['highway'] == 'primary':
    #    width = 7
    #elif road_feature.properties['highway'] == 'secondary':
    #    width = 5
    #elif road_feature.properties['highway'] == 'tertiary':
    #    width = 3
    #else:
    width = 10

    return shapely.geometry.shape(road_geometry).buffer(width)
    

image_name = sys.argv[1]
markup_name = sys.argv[2]

# Getting rid of non-ascii characters in properties (and all the properties whatsoever)
clean_markup_road(markup_name)

with rasterio.open(image_name) as src:
    tr = src.transform
    shape = [src.height, src.width]
    crs = src.crs

dir = os.path.dirname(os.path.abspath(image_name))
fc = FeatureCollection.read(markup_name).reproject(crs)
fc.apply(make_poly)
rasterize(fc, tr, shape, 'roads').save(dir)
