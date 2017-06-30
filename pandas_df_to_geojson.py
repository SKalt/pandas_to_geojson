"Functions to extract geojson from pandas.DataFrames"
import pandas as pd
import geojson
import pdb

def to_list(pd_series):
    "Shorthand: Coerce a pd.Series to a list of its elements"
    return pd_series.tolist()

def make_position(df, lat, lon):
    """
    Extract a pd.Series of [lat, lon] lists from a DataFrame df
    Args:
        df: a pandas.DataFrame
        lat: a str column name in df representing latitude
        lon: a str column name in df representing longitude
    Returns:
        a pandas.Series of [lat, lon].
    """
    return df.apply(lambda row: pd.concat([row[lat], row[lon]]).tolist())

def group_coordinates(hdf):
    """
    Heirarchically group coordinate [lat, lon] pairs into nested lists
    Args:
        hdf: a pandas.DataFrame or .Series with a hierarchical MultiIndex
    returns:
        a pandas.Series of nested lists. Note the index will be feature ids.
    """
    if 'levels' not in dir(hdf.index):
        return hdf
    levels = [i for i in range(len(hdf.index.levels))]
    aggregator = hdf
    for i in range(len(levels) -1, 0, -1):
        print(levels[:i])
        aggregator = aggregator.groupby(level=levels[:i]).apply(to_list)
    return aggregator

def df_to_geojson(pd_df, lat, lon, geometry_type, aggregation_ids=[]):
    """
    Aggregates lat, lon coordinates a pandas.DataFrame into higher geometries.
    Args:
        df: a pandas.DataFrame.  It may already have hierarchical index.
        lat: a str or int column id representing latitude
        lon: a str or int column id representing longitude
        geometry_type: either a string geojson geometry name, or a function
            yeilding a geojson object
        aggregation_ids: an iterable of str or int column ids. This *must* be in
            hierarchical order feature_id > polygon_id > interior_ring
             | linestring_id > point_id.
    Returns:
        a geojson FeatureCollection of Features
    """
    print(aggregation_ids)
    if aggregation_ids:
        if not isinstance(aggregation_ids, list):
            aggregation_ids = [aggregation_ids]
        # df is not hierarchical, and so must be aggregated
        pd_df = pd_df.groupby(aggregation_ids)
    coordinates = make_position(pd_df, lat, lon) # a hierarchical pd.Series
    coordinates = group_coordinates(coordinates) # now a series of nested lists
    feature_collection = geojson.FeatureCollection([])
    for coords in coordinates:
        if isinstance(geometry_type, str):
            geometry = {
                'type': geometry_type,
                'coordinates': coords
            }
        else:
            # assume it must be a geojson geometry factory
            geometry = geometry_type(coords)
        feature_collection['features'].append(
            geojson.Feature(geometry=geometry)
        )
    return feature_collection
