"nose tests"
import pandas as pd
from geojson import FeatureCollection, Feature, Point, LineString, Polygon, \
    MultiPoint, MultiLineString, MultiPolygon, dumps
import pandas_df_to_geojson as pd2g

def setup_point():
    return pd.DataFrame([
        [0, 100.0, 0.0]
    ], columns=['feature_id', 'x', 'y'])

def setup_points():
    return pd.DataFrame([
        [0, 100.0, 0.0],
        [1, 101.0, 1.0]
    ], columns=['feature_id', 'x', 'y'])

def setup_linestring():
    return pd.DataFrame([
        [0, 0, 100.0, 0.0],
        [0, 1, 101.0, 1.0]
    ], columns=['feature_id', 'pt_id', 'x', 'y'])

def setup_polygon():
    return pd.DataFrame([
        [0, 0, 0, 100.0, 0.0],
        [0, 0, 1, 101.0, 0.0],
        [0, 0, 2, 101.0, 1.0],
        [0, 0, 3, 100.0, 1.0],
        [0, 0, 4, 100.0, 0.0],
        [0, 1, 0, 100.2, 0.2],
        [0, 1, 1, 100.8, 0.2],
        [0, 1, 2, 100.8, 0.8],
        [0, 1, 3, 100.2, 0.8],
        [0, 1, 4, 100.2, 0.2]
    ], columns=['feature_id', 'ring_id', 'pt_id', 'x', 'y'])

def setup_multipoint():
    return pd.DataFrame([
        [0, 0, 100.0, 0.0],
        [0, 1, 101.0, 1.0]
    ], columns=['feature_id', 'pt_id', 'x', 'y'])

def setup_multilinestring():
    return pd.DataFrame([
        [0, 0, 0, 100.0, 0.0],
        [0, 0, 1, 101.0, 1.0],
        [0, 1, 0, 102.0, 2.0],
        [0, 1, 1, 103.0, 3.0]
    ], columns=['feature_id', 'line_id', 'pt_id', 'x', 'y'])

def setup_multipolygon():
    return pd.DataFrame([
        [0, 0, 0, 0, 102, 2],
        [0,0, 0, 1, 103, 2],
        [0, 0, 0, 2, 103, 3],
        [0, 0, 0, 3, 102, 3],
        [0, 0, 0, 4, 102, 2],
        [0, 1, 0, 0, 100, 0],
        [0, 1, 0, 1, 101, 0],
        [0, 1, 0, 2, 101, 1],
        [0, 1, 0, 3, 100, 1],
        [0, 1, 0, 4, 100, 0],
        [0, 1, 1, 0, 100.2, 0.2],
        [0, 1, 1, 1, 100.8, 0.2],
        [0, 1, 1, 2, 100.8, 0.8],
        [0, 1, 1, 3, 100.2, 0.8],
        [0, 1, 1, 4, 100.2, 0.2],
        [1, 0, 0, 0, 102, 2],
        [1, 0, 0, 1, 103, 2],
        [1, 0, 0, 2, 103, 3],
        [1, 0, 0, 3, 102, 3],
        [1, 0, 0, 4, 102, 2],
        [1, 1, 0, 0, 100, 0],
        [1, 1, 0, 1, 101, 0],
        [1, 1, 0, 2, 101, 1],
        [1, 1, 0, 3, 100, 1],
        [1, 1, 0, 4, 100, 0],
        [1, 1, 1, 0, 100.2, 0.2],
        [1, 1, 1, 1, 100.8, 0.2],
        [1, 1, 1, 2, 100.8, 0.8],
        [1, 1, 1, 3, 100.2, 0.8],
        [1, 1, 1, 4, 100.2, 0.2]],
        columns=['feature_id', 'poly_id', 'ring_id', 'pt_id', 'x', 'y'])

# def get_geom(geom):
#     return {
#         'Point':Point,
#         'LineString':LineString,
#         'Polygon':Polygon,
#         'MultiPoint':MultiPoint,
#         'MultiLineString':MultiLineString,
#         'MultPolygon':MultiPolygon
#         }[geom]

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def assert_equal(source, target, err_msg_insert):
    if ordered(source) != ordered(target):
        raise AssertionError(
            'case {}: Desired output not produced:\n """{}""" \n!=\n """{}"""'.format(
                err_msg_insert,
                source,
                target
            )
        )
def _test(setup, target_result, geom, agg):
    df = setup()
    assert_equal(
        pd2g.df_to_geojson(df, 'x', 'y', geom, aggregation_ids=agg),
        target_result,
        (geom)
    )

def test_point(geom='Point'):
    _test(
        setup_point,
        FeatureCollection([
            Feature(geometry=Point([100.0, 0.0]))
        ]),
        geom,
        ['feature_id']
    )
def test_points(geom='Point'):
    _test(
        setup_points,
        FeatureCollection([
            Feature(geometry=Point([100.0, 0.0])),
            Feature(geometry=Point([101.0, 1.0]))
        ]),
        geom,
        ['feature_id'],
    )
    
def test_linestring(geom='LineString'):
    _test(
        setup_linestring,
        FeatureCollection([
            Feature(geometry={
                "type": "LineString",
                "coordinates": [ [100.0, 0.0], [101.0, 1.0] ]
            })
        ]),
        geom,
        ['feature_id', 'pt_id']
    )
def test_polygon(geom='Polygon'):
    _test(
        setup_polygon,
        FeatureCollection([
            Feature(geometry={
                "type": "Polygon",
                "coordinates": [
                    [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ],
                    [ [100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2] ]
                ]
            })
        ]),
        geom,
        ['feature_id', 'ring_id', 'pt_id']
    )
def test_multipoint(geom='MultiPoint'):
    _test(
        setup_multipoint,
        FeatureCollection([
            Feature(geometry= {
                "type": "MultiPoint",
                "coordinates": [ [100.0, 0.0], [101.0, 1.0] ]
            })
        ]),
        geom,
        ['feature_id', 'pt_id']
    )
def test_multilinestring(geom='MultiLineString'):
    _test(
        setup_multilinestring,
        FeatureCollection([
            Feature(geometry={
                "type": "MultiLineString",
                "coordinates": [
                    [ [100.0, 0.0], [101.0, 1.0] ],
                    [ [102.0, 2.0], [103.0, 3.0] ]
                ]
            })
        ]),
        geom,
        ['feature_id', 'line_id', 'pt_id']
    )
def test_multipolygon(geom='MultiPolygon'):
    _test(
        setup_multipolygon,
        FeatureCollection([
            Feature(geometry={
                "type": "MultiPolygon",
                "coordinates": [
                    [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
                    [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                     [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]
                ]
            })
        ] * 2),
        geom,
        ['feature_id', 'poly_id', 'ring_id', 'pt_id']
    )

if __name__ == '__main__':
    test_point()
    test_point(Point)
    test_points()
    test_points(Point)
    test_linestring()
    test_linestring(LineString)
    test_polygon()
    test_polygon(Polygon)
    test_multipoint(MultiPoint)
    test_multipoint()
    test_multilinestring(MultiLineString)
    test_multilinestring()
    test_multipolygon(MultiPolygon)
    test_multipolygon()
