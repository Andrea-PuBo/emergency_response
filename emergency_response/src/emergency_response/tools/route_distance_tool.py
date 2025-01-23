import os
import osmnx as ox
import networkx as nx
from pathlib import Path
from crewai_tools import BaseTool
from typing import Optional, Type
from emergency_response.src.emergency_response.tools.schemas.route_distance_schema import RouteDistanceSchema

base_dir = Path(__file__).resolve().parents[3]  # Adjust based on your structure
city_map_path = os.path.join(base_dir, "data", "tarragona.graphml")

class RouteDistanceTool(BaseTool):
    name: str = "Route distance calculator"
    description: str = (
        "A tool to find the driving route distance between an origin and a destination on a map given their coordinates."
    )
    args_schema: Type[RouteDistanceSchema] = RouteDistanceSchema
    city_map: Optional[nx.MultiDiGraph] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if not city_map_path:
            raise ValueError("A valid city map path to a GraphML file must be provided.")

        # Load the map and preprocess it
        self.city_map = ox.load_graphml(city_map_path)
        self.city_map = ox.routing.add_edge_speeds(self.city_map)
        self.city_map = ox.routing.add_edge_travel_times(self.city_map)

    def _run(self, *args, **kwargs) -> int:
        """Find the driving distance between two coordinates."""
        params = args[0]
        x_origin = params.get("x_origin")
        y_origin = params.get("y_origin")
        x_destination = params.get("x_destination")
        y_destination = params.get("y_destination")

        return self._find_distance(x_origin, y_origin, x_destination, y_destination)

    def _find_distance(self, x_origin: float, y_origin: float, x_destination: float, y_destination: float) -> int:
        """Calculate the driving distance using OSMnx."""
        origin_node = ox.distance.nearest_nodes(self.city_map, X=x_origin, Y=y_origin)
        destination_node = ox.distance.nearest_nodes(self.city_map, X=x_destination, Y=y_destination)
        route = ox.shortest_path(self.city_map, origin_node, destination_node, weight="travel_time")
        edge_lengths = ox.routing.route_to_gdf(self.city_map, route)["length"]

        return round(sum(edge_lengths))

