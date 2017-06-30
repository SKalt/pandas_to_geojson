"Coerce a pd.Series to a list of its elements"
to_list = lambda pd_series: pd_series.tolist()

def make_point(df, lat, lon):
    "Extract a pd.Series of [lat, lon] lists from a DataFrame df"
    return df.apply(lambda row: to_list(pd.concat([row[lat], row[lon]])))

def group_heirarchical(hdf):
    levels = [i for i in range(len(hdf.index.levels))]
    aggregator = hdf
    for i in range(len(levels), 0, -1):
        aggregator = aggregator.groupby(level=levels[:i]).apply(to_list)
    return aggregator

def df_to_geojson(df, lat, lon, geometry_type, *aggregation_ids):
    if aggregation_ids:
        # df is not hierarchical, and so must be aggregated
        df = df.groupby(aggregation_ids)
    coordinates = make_point(df, lat, lon) # a hierarchical pd.Series
    coordinates = group_hierarchies(coordinates) # now a series of nested lists
    feature_collection = {
        'type':'FeatureCollection',
        'features':[]
        }
    for coords in coordinates:
        feature_collection['features'].append({
            'type':'Feature',
            'properties':{}, # you'll need to extract properties somehow
            'geometry': {
                'type': geometry_type,
                'coordinates': coordinates
            }
        })
    return feature_collection