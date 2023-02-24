import pandas as pd

import utils.coordinates as lib


def test_angle_str2value():
    assert lib.angle_str2value("51°53′N", precision=5) == 51.88333
    assert lib.angle_str2value("51°53′S", precision=5) == -51.88333
    assert lib.angle_str2value("51°53′E", precision=5) == 51.88333
    assert lib.angle_str2value("51°53′W", precision=5) == -51.88333


def test_coords_to_latlon_scalar():
    assert lib.coords_to_latlon_scalar("51°53′N 176°39′W") == (51.88333, -176.65)
    assert lib.coords_to_latlon_scalar("18°08′S 178°27′E") == (-18.13333, 178.45)


def test_coords_to_latlon():
    series = pd.Series([
         "51°53′N 176°39′W",
         "18°08′S 178°27′E",
    ])
    lat, lon = lib.coords_to_latlon(series, precision=3)
    pd.testing.assert_series_equal(lat, pd.Series([51.883, -18.133], name="lat"))
    pd.testing.assert_series_equal(lon, pd.Series([-176.65, 178.45], name="lon"))
