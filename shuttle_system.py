import json
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVER_ROSTER = {"R1": "Prakash", "R2": "Leela", "R3": "Imran"}

def add_trip_log(route_id, passenger_count, logs=[]):
    if route_id not in routes:
        raise KeyError("Unknown route: %s" % route_id)
    if isinstance(passenger_count, bool) or not isinstance(passenger_count, int) or passenger_count < 0:
        raise ValueError("Invalid passenger count for %s: %r" % (route_id, passenger_count))
    routes[route_id]["trips"].append(passenger_count)
    logs.append("%s: %s carried %s" % (datetime.now(), route_id, passenger_count))
    return logs

def remove_route(route_id):
    del routes[route_id]

def average_load(route_id):
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)

def underused_routes():
    flagged = []
    for r in routes:
        avg = average_load(r)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(r)
    return flagged

def assignDriver(route_id):
    return DRIVER_ROSTER.get(route_id, "Tom")

def sync_fleet_data(file="fleet.json"):
    global routes
    f = open(file, "w")
    f.write(json.dumps(routes))
    f.close()
    f = open(file)
    routes = json.loads(f.read())

def main():
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    for bad_route, bad_count in (("R2", -6), ("R3", "full")):
        try:
            add_trip_log(bad_route, bad_count)
        except ValueError as err:
            print("Rejected:", err)
    add_trip_log("R3", 12)
    print("Driver for R1:", assignDriver("R1"))
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

main()
