import re
from typing import Optional, Tuple, Union

import pandas as pd
import utm

ANGLE_RE = '^(?P<degree>\d+)°(?P<minute_of_arc>\d+)′(?P<letter>.)$'


def angle_str2value(angle_str: str, precision: Optional[int] = None) -> float:
    """Convert an angle of coordinates to value"""
    search = re.match(ANGLE_RE, angle_str)
    if not search:
        raise ValueError(f'Given angle representation {angle_str!r} does not match {ANGLE_RE!r}')
    sign = 1 if search.group('letter') in ['N', 'E'] else -1
    value = sign * (
        int(search.group('degree'))
        + int(search.group('minute_of_arc')) / 60
    )
    if precision:
        value = round(value, precision)
    return value


def coords_to_latlon_scalar(coords: str, precision: Optional[int] = 5) -> Tuple[float, float]:
    """Convert coordinates string to latitude, longitude"""
    lat_str, lon_str = coords.split(' ')
    return angle_str2value(lat_str, precision), angle_str2value(lon_str, precision)


def coords_to_latlon(coords: pd.Series, precision: Optional[int] = 5) -> Tuple[pd.Series, pd.Series]:
    """Convert coordinates string to latitude, longitude"""
    latlon = coords.str.split(' ', 2, expand=True).rename({0: 'lat', 1: 'lon'}, axis=1)
    latlon = latlon.applymap(angle_str2value, precision=precision)
    return latlon.lat, latlon.lon


def coords_to_xy(coords: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """Convert coordinates string to latitude, longitude"""
    lat, lon = coords_to_latlon(coords, precision=None)
    x, y, _, _ = utm.from_latlon(lat.values, lon.values)
    return pd.Series(x, name='x'), pd.Series(y, name='y')
