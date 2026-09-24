import json
import math
import sys


def load_data(filename):
    """Load and parse a JSON input file."""

    with open(filename, "r") as file:
        data = json.load(file)

    return data


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""

    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2
    )

    return distance


def find_nearest_agent(warehouse, agents):
    """Find the agent closest to the given warehouse."""

    nearest_agent = None
    minimum_distance = float("inf")

    for agent in agents:

        distance = calculate_distance(
            agent["location"],
            warehouse["location"]
        )

        if distance < minimum_distance:
            minimum_distance = distance
            nearest_agent = agent

    return nearest_agent


def assign_packages(packages, warehouses, agents):
    """Assign each package to the nearest agent."""

    assignments = []

    for package in packages:

        warehouse_id = package["warehouse_id"]

        # Find the warehouse corresponding to this package.
        warehouse = None

        for warehouse_item in warehouses:

            if warehouse_item["id"] == warehouse_id:
                warehouse = warehouse_item
                break

        # Find the nearest agent to the package's warehouse.
        nearest_agent = find_nearest_agent(
            warehouse,
            agents
        )

        # Store the package-agent assignment.
        assignment = {
            "package": package,
            "agent": nearest_agent
        }

        assignments.append(assignment)

    return assignments


def simulate_delivery(assignments, warehouses):
    """Simulate package pickup and delivery for each agent."""

    agent_data = {}

    for assignment in assignments:

        package = assignment["package"]
        agent = assignment["agent"]

        agent_id = agent["id"]

        # Create a record for this agent if it does not exist.
        if agent_id not in agent_data:

            agent_data[agent_id] = {
                "current_location": agent["location"],
                "packages_delivered": 0,
                "total_distance": 0.0
            }

        # Get the agent's current location.
        current_location = agent_data[agent_id]["current_location"]

        # Find the warehouse for this package.
        warehouse = None

        for warehouse_item in warehouses:

            if warehouse_item["id"] == package["warehouse_id"]:
                warehouse = warehouse_item
                break

        warehouse_location = warehouse["location"]

        # Distance from agent's current location to warehouse.
        distance_to_warehouse = calculate_distance(
            current_location,
            warehouse_location
        )

        # Add this distance to the agent's total.
        agent_data[agent_id]["total_distance"] += distance_to_warehouse

        # Agent is now at the warehouse.
        agent_data[agent_id]["current_location"] = warehouse_location

        # Calculate distance from warehouse to destination.
        distance_to_destination = calculate_distance(
            warehouse_location,
            package["destination"]
        )

        # Add this distance to the agent's total.
        agent_data[agent_id]["total_distance"] += distance_to_destination

        # Agent is now at the package destination.
        agent_data[agent_id]["current_location"] = package["destination"]

        # Increase delivered package count.
        agent_data[agent_id]["packages_delivered"] += 1

    return agent_data


def generate_report(results):
    """Generate the final delivery report."""

    report = {}

    best_agent = None
    best_efficiency = float("inf")

    for agent_id, result in results.items():

        packages_delivered = result["packages_delivered"]
        total_distance = result["total_distance"]

        # Calculate average distance per delivered package.
        efficiency = total_distance / packages_delivered

        # Store the agent's report.
        report[agent_id] = {
            "packages_delivered": packages_delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": round(efficiency, 2)
        }

        # Lower distance per package means higher efficiency.
        if efficiency < best_efficiency:
            best_efficiency = efficiency
            best_agent = agent_id

    # Add the best agent to the report.
    report["best_agent"] = best_agent

    return report


def save_report(report, filename):
    """Save the report as a JSON file."""

    with open(filename, "w") as file:
        json.dump(report, file, indent=4)


def validate_delivery(packages, results):
    """Check whether all input packages were delivered."""

    total_packages = len(packages)

    delivered_packages = 0

    for result in results.values():
        delivered_packages += result["packages_delivered"]

    print("\nDelivery validation:")
    print("Total packages:", total_packages)
    print("Delivered packages:", delivered_packages)

    if total_packages == delivered_packages:
        print("Status: PASS")
        return True
    else:
        print("Status: FAIL")
        return False


def main():

    # -----------------------------
    # SELECT INPUT JSON FILE
    # -----------------------------

    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
    else:
        input_filename = "base_case.json"

    data = load_data(input_filename)

    print("Input file:", input_filename)


    # -----------------------------
    # PART 1: Load JSON data
    # -----------------------------

    print("\nWarehouses:")
    print(data["warehouses"])

    print("\nAgents:")
    print(data["agents"])

    print("\nPackages:")
    print(data["packages"])


    # -----------------------------
    # PART 2: Calculate distance
    # -----------------------------

    print("\nDistances from agents to W1:")

    warehouse_w1 = data["warehouses"][0]["location"]

    for agent in data["agents"]:

        agent_location = agent["location"]

        distance = calculate_distance(
            agent_location,
            warehouse_w1
        )

        print(
            agent["id"],
            "-> W1:",
            round(distance, 2)
        )


    # -----------------------------
    # PART 3: Find nearest agents
    # -----------------------------

    print("\nNearest agents:")

    for warehouse in data["warehouses"]:

        nearest_agent = find_nearest_agent(
            warehouse,
            data["agents"]
        )

        print(
            warehouse["id"],
            "->",
            nearest_agent["id"]
        )


    # -----------------------------
    # PART 4: Assign packages
    # -----------------------------

    assignments = assign_packages(
        data["packages"],
        data["warehouses"],
        data["agents"]
    )

    print("\nPackage assignments:")

    for assignment in assignments:

        print(
            assignment["package"]["id"],
            "->",
            assignment["agent"]["id"]
        )


    # -----------------------------
    # PART 5: Simulate delivery
    # -----------------------------

    results = simulate_delivery(
        assignments,
        data["warehouses"]
    )

    print("\nDelivery results:")

    for agent_id, result in results.items():

        print(
            agent_id,
            "-> Packages:",
            result["packages_delivered"],
            "Distance:",
            round(result["total_distance"], 2)
        )


    # -----------------------------
    # PART 6: Generate report
    # -----------------------------

    report = generate_report(results)

    print("\nFinal report:")

    print(json.dumps(report, indent=4))


    # -----------------------------
    # PART 7: Validate delivery
    # -----------------------------

    validate_delivery(
        data["packages"],
        results
    )


    # -----------------------------
    # SAVE REPORT
    # -----------------------------

    save_report(
        report,
        "report.json"
    )

    print("\nReport saved to report.json")


if __name__ == "__main__":
    main()