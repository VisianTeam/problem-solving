from typing import Dict, Iterable, Set
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

GraphSegment = Tuple[int, int]  # index of origin, index of destination
Coords = Tuple[float, float]


class Cities:
    """Container of list of cities with their details"""

    def __init__(self, path: str):
        """Create instance from file

        Example: `cities = Cities("data/cities.csv")`
        """
        self.df: pd.DataFrame = pd.read_csv(path)
        self._coords: Optional[pd.DataFrame] = None

    @property
    def coords(self) -> pd.DataFrame:
        """dataframe with cities coordinates

        Return:
            pd.DataFrame with columns ['city', 'x', 'y']
        """
        if self._coords is None:
            self._coords = self._build_coordinates()
        return self._coords

    @property
    def index(self) -> pd.Index:
        return self.df.index

    def get_city_name(self, city_index: int) -> str:
        """Return coordinates of city given its index/name"""
        city = self.df.loc[city_index]
        return city['City']

    def get_city_xy(self, city_index: int) -> Coords:
        """Return coordinates of city given its index/name"""
        city = self.coords.loc[city_index]
        return city.x, city.y

    # ---- Management

    def filter(self, names: List[str], reset_index: bool = True) -> None:
        """Filter cities on cities in names"""
        self.df = self.df[self.df['City'].isin(names)]
        if reset_index:
            self.df.reset_index(inplace=True)

    def _build_coordinates(self) -> pd.DataFrame:
        """Convert detailed table of cities (source data) to database"""
        lat = self.df['Near Latitude'].values * np.pi/180
        lon = self.df['Near Longitude'].values * np.pi/180

        earth_radius = 6371
        return pd.DataFrame({
            'city': self.df['City'].values,
            'x': earth_radius*np.cos(lat)*np.cos(lon),
            'y': earth_radius*np.cos(lat)*np.sin(lon),
        }, index=self.df.index)


class Connection:
    """A connection between 2 cities"""
    __slots__ = (
        'origin',
        'destin',
        'distance',
        'origin_name',
        'destin_name',
    )

    def __init__(
            self,
            origin: int,
            destin: int,
            distance: float,
            origin_name: Optional[str] = None,
            destin_name: Optional[str] = None,
    ):
        self.origin = origin
        self.destin = destin
        self.distance = distance
        self.origin_name: str = str(origin) if origin_name is None else origin_name
        self.destin_name: str = str(destin) if destin_name is None else destin_name

    @property
    def segment(self) -> GraphSegment:
        """segment of connection"""
        return self.origin, self.destin

    def tuple(self):
        """tuple representation of connection"""
        return self.origin, self.destin, self.destin

    def __eq__(self, other):
        return self.tuple() == other.tuple()

    def __hash__(self):
        return hash(self.tuple())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            f"Connection("
            f"{self.origin}:{self.origin_name!r}"
            f" to {self.destin}:{self.destin_name!r}"
            f")"
        )


class CitiesGraph:
    """Container for list of connected cities"""

    @classmethod
    def from_file(cls, path: str, names: Optional[List[str]] = None) -> 'CitiesGraph':
        """Create graph of cities from csv file

        Example: `graph = CitiesGraph.from_file(path, [ "Dallas", "Detroit"])`
        """
        cities = Cities(path)
        if names:
            cities.filter(names)
        return cls(cities)

    def __init__(self, cities: Cities):
        """Initiate graph of cities with empty connections"""
        self.cities: Cities = cities
        self.connections: Set[Connection] = set()

    def get_nodes(self) -> List[int]:
        """Return list of indexes of cities"""
        return self.cities.index.tolist()

    # ---- Connections

    def create_connection(
            self,
            origin: int,
            destin: int,
            distance: Optional[float] = None,
    ):
        """Create connection between 2 cities"""
        if distance is None:
            xo, yo = self.cities.get_city_xy(origin)
            xd, yd = self.cities.get_city_xy(destin)
            distance = np.sqrt((xo - xd)**2 + (yo - yd)**2)
        self.connections.add(Connection(
            origin,
            destin,
            distance,
            origin_name=self.cities.get_city_name(origin),
            destin_name=self.cities.get_city_name(destin),
        ))

    def fully_connect(self):
        """Fully connect the graph"""
        nodes = self.get_nodes()
        for i, origin in enumerate(nodes):
            for destin in nodes[i+1:]:
                self.create_connection(origin, destin)

    def get_distances_by_segments(self) -> Dict[GraphSegment, Connection]:
        """Return dictionary of graph segments with associated distances"""
        return {
            conn.segment: conn.distance
            for conn in self.connections

        }

    # ---- Plot

    def plot_line(self, points: List[int], **kwargs) -> None:
        """Plot continuous line between points (given their index in coords)"""
        return self.plot_segments(zip(points[:-1], points[1:]), **kwargs)

    def plot_segments(self, segments: Iterable[GraphSegment], **kwargs) -> None:
        """Plot a list of segments"""
        for origin, destin in segments:
            self.plot_segment(origin, destin, **kwargs)

    def plot_segment(self, origin: int, destination: int, **kwargs) -> None:
        """Plot a segment"""
        xo, yo = self.cities.get_city_xy(origin)
        xd, yd = self.cities.get_city_xy(destination)
        plt.plot((xo, xd), (yo, yd), **kwargs)

    def plot_connections(self, **kwargs):
        """Plot every existing connections"""
        self.plot_segments([conn.segment for conn in self.connections], **kwargs)

    def plot_points(self, with_index: bool = False) -> None:
        """Plot cities points with their labels"""
        X = self.cities.coords['x']
        Y = self.cities.coords['y']
        T = self.cities.coords['city']
        if with_index:
            T = self.cities.index.to_series().apply(str) + ". " + T

        fix, ax = plt.subplots()
        ax.scatter(X, Y)
        for x, y, t in zip(X, Y, T):
            ax.annotate(t, (x, y))
