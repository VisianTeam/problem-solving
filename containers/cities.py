from typing import Iterable, Set, Union

import pandas as pd
from matplotlib import pyplot as plt

Loc = Union[int, str]

import numpy as np
from typing import List, Optional, Tuple


def filter_cities(df: pd.DataFrame, names: List[str]) -> pd.DataFrame:
    """Filter cities on cities in names"""
    return df[df["City"].isin(names)]


def get_coordinates(
        df: pd.DataFrame,
        names: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Convert detailed table of cities (source data) to database"""
    if names:
        df = filter_cities(df, names)

    lat = df["Near Latitude"].values * np.pi/180
    lon = df["Near Longitude"].values * np.pi/180

    earth_radius = 6371
    return pd.DataFrame({
        "city": df["City"].values,
        "x": earth_radius*np.cos(lat)*np.cos(lon),
        "y": earth_radius*np.cos(lat)*np.sin(lon),
    })


class CitiesGraph:
    """Container for list of connected cities"""

    @classmethod
    def from_file(cls, path: str, cities: Optional[List[str]] = None) -> "CitiesGraph":
        """Create graph of cities from csv file

        Example of file at data/cities.csv
        """
        cities_df = pd.read_csv(path)
        coordinates = get_coordinates(cities_df, names=cities)
        return cls(coordinates)

    def __init__(self, coordinates: pd.DataFrame):
        """Initiate graph of cities with empty connections"""
        self.coords: pd.DataFrame = coordinates
        self.connections: Set[Tuple[int, int]] = set()

    def fully_connect(self):
        """Fully connect the graph"""
        indexes = self.coords.index.tolist()
        for i, origin in enumerate(indexes):
            for j, destin in enumerate(indexes[i+1:], i+1):
                self.connections.add((origin, destin))

    def get_city_xy(self, loc: Loc) -> Tuple[float, float]:
        """Return coordinates of city given its index/name"""
        if isinstance(loc, str):
            city_df = self.coords[self.coords["city"] == loc]
            assert len(city_df) == 1
            city = city_df.iloc[0]
        else:
            city = self.coords.loc[loc]
        return city.x, city.y

    def plot_line(self, points: List[Loc], **kwargs) -> None:
        """Plot continuous line between points"""
        return self.plot_segments(zip(points[:-1], points[1:]), **kwargs)

    def plot_segments(self, segments: Iterable[Tuple[Loc, Loc]], **kwargs) -> None:
        """Plot a list of segments"""
        for origin, destinatation in segments:
            self.plot_segment(origin, destinatation, **kwargs)

    def plot_segment(self, origin: Loc, destination: Loc, **kwargs) -> None:
        """Plot a segment"""
        xo, yo = self.get_city_xy(origin)
        xd, yd = self.get_city_xy(destination)
        plt.plot((xo, xd), (yo, yd), **kwargs)

    def plot_connections(self, **kwargs):
        """Plot every existing connections"""
        self.plot_segments(self.connections, **kwargs)

    def plot_points(self) -> None:
        """Plot cities points with their labels"""
        X = self.coords["x"]
        Y = self.coords["y"]
        T = self.coords["city"]

        fix, ax = plt.subplots()
        ax.scatter(X, Y)
        for x, y, t in zip(X, Y, T):
            ax.annotate(t, (x, y))