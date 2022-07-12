# Import a CSV dataset of features to display, optionally join it with an existing feature GeoJSON file, and generate a new GeoJSON file as output.
#
# usage:
#    python3 importcsv.py INPUT_FILENAME OUTPUT_FILENAME [JOIN_FILENAME]
#
# where INPUT_FILENAME is a CSV, OUTPUT_FILENAME is a GeoJSON output file,
# and JOIN_FILENAME is a prior version of the GeoJSON output file containing label_x, label_y and label_callout
# attributes to be preserved.

import sys
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
  
# Read in a CSV file with a header including these prescribed columns:
#   longitude, latitude: geographic coordinates of file
#   sid: unique ID of station
#   type: one of ['launch','destination','current','tide']
#   title: full title of CSV
#   chart_title: optional chart-specific label if different from the full title

df = pd.read_csv(sys.argv[1])   # input CSV
dfd = df.drop(['longitude','latitude'],axis=1)  # create view of CSV dataframe without lat/long
dfgeom = [Point(xy) for xy in zip(df.longitude, df.latitude)]  # list of geometries for the CSV

# convert all of the above to a GeoDataFrame
gdfin = gpd.GeoDataFrame(dfd, crs='epsg:4326', geometry=dfgeom)

schema = {
    'geometry': 'Point',
    'properties': {
        'sid': 'str',
        'title': 'str',
        'chart_title': 'str',
        'type': 'str',
        'label_x': 'float',
        'label_y': 'float',
        'label_callout': 'bool'
    }
}

if len(sys.argv) - 1 < 3:
    # we are not joining with existing data, so add dummy label_x and label_y columns
    gdfin.insert(len(gdfin.columns),'label_x',float('NaN'))
    gdfin.insert(len(gdfin.columns),'label_y',float('NaN'))
    gdfin.insert(len(gdfin.columns),'label_callout',False)
    gdfout = gdfin
else:
    # join to an existing dataset with label_x and label_y attributes that are to be preserved
    gdfjoin = gpd.read_file(sys.argv[3], schema=schema)
    gdflabelxy = pd.DataFrame(gdfjoin,columns=['sid','label_x','label_y','label_callout']).set_index('sid')
    gdfout = gdfin.join(gdflabelxy, on='sid', how='left')

# write the output file
gdfout.to_file(sys.argv[2],crs='EPSG:4326',schema=schema)
