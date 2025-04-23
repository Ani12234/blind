from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Dict, Optional, Tuple
import logging
import math

class LocationAwareness:
    def __init__(self, user_agent: str = "visionmate"):
        """
        Initialize the location awareness system.
        
        Args:
            user_agent: User agent string for the geocoding service
        """
        self.geolocator = Nominatim(user_agent=user_agent)
        self.logger = logging.getLogger(__name__)
        
    def get_location_context(self, latitude: float, longitude: float) -> Dict:
        """
        Get contextual information about the current location.
        
        Args:
            latitude: Current latitude
            longitude: Current longitude
            
        Returns:
            Dictionary containing location context information
        """
        try:
            location = self.geolocator.reverse(f"{latitude}, {longitude}")
            if location:
                return {
                    "address": location.address,
                    "raw": location.raw,
                    "latitude": latitude,
                    "longitude": longitude
                }
            return {
                "latitude": latitude,
                "longitude": longitude,
                "address": "Unknown location"
            }
        except Exception as e:
            self.logger.error(f"Error getting location context: {e}")
            return {
                "latitude": latitude,
                "longitude": longitude,
                "address": "Error getting location information"
            }
    
    def calculate_distance(self, 
                         point1: Tuple[float, float], 
                         point2: Tuple[float, float]) -> float:
        """
        Calculate the distance between two points in meters.
        
        Args:
            point1: Tuple of (latitude, longitude) for first point
            point2: Tuple of (latitude, longitude) for second point
            
        Returns:
            Distance in meters
        """
        try:
            return geodesic(point1, point2).meters
        except Exception as e:
            self.logger.error(f"Error calculating distance: {e}")
            return 0.0
    
    def get_direction(self, 
                     current: Tuple[float, float], 
                     target: Tuple[float, float]) -> str:
        """
        Get the cardinal direction from current location to target.
        
        Args:
            current: Tuple of (latitude, longitude) for current location
            target: Tuple of (latitude, longitude) for target location
            
        Returns:
            Cardinal direction (N, NE, E, SE, S, SW, W, NW)
        """
        try:
            lat1, lon1 = current
            lat2, lon2 = target
            
            # Calculate bearing
            d_lon = lon2 - lon1
            y = math.sin(d_lon) * math.cos(lat2)
            x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
            bearing = math.degrees(math.atan2(y, x))
            
            # Convert bearing to cardinal direction
            directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            index = round(bearing / 45) % 8
            return directions[index]
        except Exception as e:
            self.logger.error(f"Error calculating direction: {e}")
            return "unknown"
    
    def generate_location_description(self, context: Dict) -> str:
        """
        Generate a natural language description of the current location.
        
        Args:
            context: Location context dictionary
            
        Returns:
            Natural language description of the location
        """
        try:
            address = context.get("address", "Unknown location")
            return f"You are currently at {address}"
        except Exception as e:
            self.logger.error(f"Error generating location description: {e}")
            return "Unable to determine current location" 