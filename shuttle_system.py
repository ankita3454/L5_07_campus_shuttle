"""Campus shuttle timetable and fleet tracker.

Logs passenger counts per trip, computes average loads, flags
under-used routes and syncs fleet data to a JSON file.
"""
import json
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVER_ROSTER = {"R1": "Prakash", "R2": "Leela", "R3": "Imran"}

def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip for a route and return the trip log list."""
    if logs is None:
        logs = []
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    if (isinstance(passenger_count, bool)
            or not isinstance(passenger_count, int) or passenger_count < 0):
        raise ValueError(
            f"Invalid passenger count for {route_id}: {passenger_count!r}")
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs

def remove_route(route_id):
    """Delete a route from the fleet."""
    del routes[route_id]

def average_load(route_id):
    """Return the mean passengers per trip, or None if no trips."""
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)

def underused_routes():
    """Return route ids whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in routes:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged

def assign_driver(route_id):
    """Return the rostered driver for a route."""
    return DRIVER_ROSTER.get(route_id, "Tom")

def sync_fleet_data(path="fleet.json"):
    """Write fleet data to disk and reload it into the routes dict."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(routes, handle)
    with open(path, encoding="utf-8") as handle:
        loaded = json.load(handle)
    routes.clear()
    routes.update(loaded)

def main():
    """Run a short demo of the shuttle tracker."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    for bad_route, bad_count in (("R2", -6), ("R3", "full")):
        try:
            add_trip_log(bad_route, bad_count)
        except ValueError as err:
            print("Rejected:", err)
    add_trip_log("R3", 12)
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    print("R3 average:", average_load("R3"))
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ").strip().upper() or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("No such route:", choice)

if __name__ == "__main__":
    main()
