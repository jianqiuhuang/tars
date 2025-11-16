"""MTA Bus API utility functions"""
import requests
import os
from enum import Enum
from datetime import datetime
from zoneinfo import ZoneInfo


# Configuration
API_KEY = os.getenv('MTA_API_KEY', '966f0407-93de-4c6f-bb59-5814d89e3278')
API_URL = "http://bustime.mta.info/api/siri/stop-monitoring.json"


class BusStop(Enum):
    ROSSVILLE_CORRELL = 'MTA_203532'
    VETERANS_BLOOMINGDALE = 'MTA_805173'
    AVE8_ST42 = 'MTA_401851'


class Bus(Enum):
    S74 = 'S74'
    S79 = 'S79'
    SIM25 = 'SIM25'
    SIM26 = 'SIM26'


def get_next_bus_arrival_times(bus_stop: BusStop, bus_id: Bus, max_distance_in_miles: int = 5, output_func=print):
    """
    Fetches and prints the "minutes away" for all buses approaching a specific stop.
    
    Args:
        bus_stop: The bus stop enum
        bus_id: The bus route enum
        max_distance_in_miles: Maximum distance to show buses
        output_func: Function to use for output (default: print)
    """
    params = {
        'key': API_KEY,
        'MonitoringRef': bus_stop.value,
        'StopMonitoringDetailLevel': 'minimum'
    }
    
    ET_TIMEZONE = ZoneInfo("America/New_York")
    
    try:
        now = datetime.now(ET_TIMEZONE)
        output_func(f"=== 🚌 Next {bus_id.value} Buses for Stop {bus_stop.name} ===")
        output_func(f"Current Time: {now.strftime('%I:%M:%S %p')}\n")
        
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        stop_visits = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
        
        if not stop_visits:
            output_func(f"No buses are currently scheduled to arrive at stop {bus_stop.value}.")
            return
        
        distinct_buses = set()
        
        for bus in stop_visits:
            journey = bus['MonitoredVehicleJourney']
            arrival = journey['MonitoredCall']
            
            route_name = journey['LineRef'].split('_')[-1]
            destination = journey['DestinationName']
            distance_text = arrival['Extensions']['Distances']['PresentableDistance']
            distance_in_miles = arrival['Extensions']['Distances']['DistanceFromCall'] * 0.000621371
            
            if route_name != bus_id.value or distance_in_miles >= max_distance_in_miles or (route_name, distance_in_miles) in distinct_buses:
                continue
            
            distinct_buses.add((route_name, distance_in_miles))
            output_func(f"Route: {route_name} (to {destination})")
            output_func(f"  Status: {distance_text}")
            output_func(f"  Calculated distance: {distance_in_miles}")
            
            if 'ExpectedArrivalTime' in arrival and arrival['ExpectedArrivalTime']:
                arrival_time = datetime.fromisoformat(arrival['ExpectedArrivalTime'])
                time_diff_seconds = (arrival_time - now).total_seconds()
                minutes_away = int(time_diff_seconds / 60)
                
                if minutes_away < 0:
                    output_func("  Arrival: Arriving now (or just departed)")
                elif minutes_away == 0:
                    output_func("  Arrival: < 1 minute away")
                else:
                    output_func(f"  Arrival: {minutes_away} min away (at {arrival_time.strftime('%I:%M %p')})")
            else:
                if 'AimedArrivalTime' in arrival and arrival['AimedArrivalTime']:
                    scheduled_time = datetime.fromisoformat(arrival['AimedArrivalTime'])
                    output_func(f"  Arrival: Scheduled for {scheduled_time.strftime('%I:%M %p')} (no live data)")
            
            output_func("-" * 20)
            
    except requests.exceptions.RequestException as e:
        output_func(f"Error fetching data from the MTA API: {e}")
    except (KeyError, IndexError):
        output_func("Could not parse the API response. This may mean no buses are running.")
    except Exception as e:
        output_func(f"An error occurred: {e}")
    output_func("=" * 20)


def run_all_bus_checks(output_func=print):
    """Run all configured bus arrival checks"""
    if API_KEY == 'YOUR_API_KEY' or not API_KEY:
        output_func("Please set your MTA_API_KEY in your environment variables")
        output_func("or replace 'YOUR_API_KEY' in the script with your actual key.")
    else:
        get_next_bus_arrival_times(BusStop.VETERANS_BLOOMINGDALE, Bus.SIM26, output_func=output_func)
        get_next_bus_arrival_times(BusStop.ROSSVILLE_CORRELL, Bus.SIM25, output_func=output_func)
        get_next_bus_arrival_times(BusStop.AVE8_ST42, Bus.SIM25, output_func=output_func)
        get_next_bus_arrival_times(BusStop.AVE8_ST42, Bus.SIM26, output_func=output_func)
        get_next_bus_arrival_times(BusStop.ROSSVILLE_CORRELL, Bus.S74, output_func=output_func)

