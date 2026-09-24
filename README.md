# Mystery Delivery System

A Python-based logistics simulation system for FastBox that assigns packages to the nearest delivery agent, simulates package delivery, calculates travel distances, and generates a delivery performance report.

## Features

- Reads delivery data from a JSON file
- Parses warehouses, delivery agents, and packages
- Calculates Euclidean distance between two locations
- Assigns each package to the nearest delivery agent
- Simulates package pickup and delivery
- Tracks the total distance travelled by each agent
- Calculates delivery efficiency for each agent
- Identifies the most efficient agent
- Validates that all packages have been delivered
- Generates and saves the final report as 'report.json'
- Supports different JSON input files

## Project Structure


mystery/
│
├── delivery_system.py     # Main Python program
├── base_case.json         # Base input data
├── report.json            # Generated delivery report
├── test_case_1.json       # Test input
├── test_case_2.json       # Test input
├── test_case_3.json       # Test input
├── test_case_4.json       # Test input
├── test_case_5.json       # Test input
├── test_case_6.json       # Test input
├── test_case_7.json       # Test input
├── test_case_8.json       # Test input
├── test_case_9.json       # Test input
├── test_case_10.json      # Test input
└── README.md              # Project documentation


## Requirements

- Python 3.10 or higher
- No external Python libraries are required
- The project uses Python standard library modules:
  - json
  - math
  - sys

## Setup

### 1. Clone or download the project

Download the project and open the project folder in a terminal or VS Code.

### 2. Check Python version

Run: python --version

Python 3.10 or higher is recommended.

### 3. Navigate to the project director

cd mystery

### 4. Run the program

To run the program using the default base case:

python delivery_system.py

The program uses 'base_case.json' as the default input file.

### 5. Run with a different input file

A different JSON file can be provided as a command-line argument:

python delivery_system.py test_case_1.json

For example:

python delivery_system.py test_case_5.json

The program will process the selected input file and generate a new 'report.json'.

## Input Format

The program accepts a JSON file containing three main sections:

- warehouses
- agents
- packages

### Example Input

'''json
{
    "warehouses": [
        {
            "id": "W1",
            "location": [0, 0]
        },
        {
            "id": "W2",
            "location": [50, 75]
        },
        {
            "id": "W3",
            "location": [100, 25]
        }
    ],
    "agents": [
        {
            "id": "A1",
            "location": [5, 5]
        },
        {
            "id": "A2",
            "location": [60, 60]
        },
        {
            "id": "A3",
            "location": [95, 30]
        }
    ],
    "packages": [
        {
            "id": "P1",
            "warehouse_id": "W1",
            "destination": [30, 40]
        },
        {
            "id": "P2",
            "warehouse_id": "W2",
            "destination": [70, 90]
        },
        {
            "id": "P3",
            "warehouse_id": "W3",
            "destination": [105, 20]
        },
        {
            "id": "P4",
            "warehouse_id": "W1",
            "destination": [10, 10]
        },
        {
            "id": "P5",
            "warehouse_id": "W2",
            "destination": [40, 80]
        }
    ]
}
'''
### Data Fields

#### Warehouses
|-------|-------------|
| Field | Description |
|-------|-------------|
| id  | Unique warehouse identifier |
| location | Warehouse coordinates in '[x, y]' format |

#### Agents
|-------|-------------|
| Field | Description |
|-------|-------------|
| id    | Unique agent identifier |
| location | Agent's starting coordinates in '[x, y]' format |

#### Packages
|-------|-------------|
| Field | Description |
|-------|-------------|
| id    | Unique package identifier |
| warehouse_id | ID of the warehouse where the package is available |
| destination  | Package delivery coordinates in '[x, y]' format |

## How the System Works

The system processes the delivery operation in the following steps:

### 1. Load the Input Data

The program reads the selected JSON file using Python's built-in 'json' module.

If no input file is provided, the program uses: base_case.json

If an input file is provided through the command line, that file is used instead.

### 2. Normalize the Input Data

The program converts supported input variations into a common internal format.

For example, warehouse and agent data can be represented as either lists of objects or dictionaries. The program normalizes these structures before processing them.

Package warehouse references are also normalized to use: warehouse_id

This allows the rest of the program to work with a consistent data structure.

### 3. Calculate Distance

The system uses Euclidean distance to calculate the distance between two coordinates.

For two points:

(x1, y1)
(x2, y2)

the distance is calculated as:
distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)

The calculation is implemented using Python's 'math' module.

### 4. Find the Nearest Agent

For each package, the program identifies its warehouse.

It then calculates the distance from every agent's starting location to that warehouse.

The agent with the smallest distance is selected for that package.


Package -> Warehouse -> Calculate distance to each agent -> Select nearest agent


### 5. Assign Packages

Each package is assigned to the nearest delivery agent.

The assignment is stored together with the package information so that it can be used during the delivery simulation.

Example:

P1 -> A1
P2 -> A2
P3 -> A3


### 6. Simulate Delivery

After package assignment, the system simulates the delivery process.

For each assigned package, the agent travels:

Current Location -> Warehouse -> Destination


The distance from the agent's current location to the warehouse is calculated first.

Then the distance from the warehouse to the package destination is calculated.

Both distances are added to the agent's total travelled distance.

The agent's current location is then updated to the package destination.

### 7. Track Agent Performance

For each agent, the system tracks:

- Number of packages delivered
- Total distance travelled

After all packages are processed, these values are used to generate the final report.

### 8. Calculate Efficiency

The system calculates efficiency using:

Efficiency = Total Distance / Packages Delivered


A lower distance per delivered package represents a lower average travel distance per package.

The agent with the lowest calculated efficiency value is recorded as: best_agent


### 9. Validate Deliveries

The program compares Total input packages with Total delivered packages

If both numbers match, the validation status is: PASS
Otherwise, the status is: FAIL


### 10. Generate the Final Report

After the simulation is complete, the system generates a report containing each agent's:

- Packages delivered
- Total distance
- Efficiency

The report also contains the 'best_agent'.

The final report is saved as: report.json

## Assumptions

The following assumptions are used to handle parts of the simulation that are not explicitly defined in the assignment:

1. Each package is assigned to the agent whose starting location is closest to the package's warehouse.
2. Euclidean distance is used to calculate the distance between two locations.
3. Each agent starts from the location provided in the input JSON.
4. Packages are processed in the same order in which they appear in the input JSON.
5. When an agent has multiple packages, the agent travels from its current location to the package's warehouse and then from the warehouse to the package's destination.
6. After delivering a package, the agent's current location becomes that package's destination.
7. The agent does not return to its original location after completing a delivery.
8. No additional travel is added after the final package delivery.
9. Efficiency is calculated as: Total Distance / Packages Delivered

10. The agent with the lowest distance per delivered package is recorded as 'best_agent'.
11. All packages are expected to be successfully delivered. The program validates this by comparing the total number of input packages with the total number of delivered packages.
12. No traffic, weather, vehicle, or other real-world constraints are considered in the basic simulation.

## Output / Sample Report

After the delivery simulation is completed, the program generates a delivery report and saves it as: report.json

### Report Format

The generated report contains information about each agent that is assigned at least one package:

- packages_delivered — Number of packages delivered by the agent
- total_distance — Total distance travelled by the agent
- efficiency — Average distance travelled per delivered package
- best_agent — Agent with the lowest distance per delivered package

### Example Report

json:
{
    "A1": {
        "packages_delivered": 2,
        "total_distance": 121.21,
        "efficiency": 60.61
    },
    "A2": {
        "packages_delivered": 2,
        "total_distance": 79.21,
        "efficiency": 39.6
    },
    "A3": {
        "packages_delivered": 1,
        "total_distance": 14.14,
        "efficiency": 14.14
    },
    "best_agent": "A3"
}


### Output Fields
|-------|-------------|
| Field | Description |
|-------|-------------|
| packages_delivered | Total number of packages delivered by the agent |
| total_distance | Total distance travelled by the agent |
| efficiency | Total distance divided by the number of packages delivered |
| best_agent | Agent with the lowest distance per delivered package |

The report is formatted as JSON with indentation for readability.

The 'report.json' file is overwritten each time the program is executed.

## Testing

The program was tested using the base case and 10 additional test cases with different input configurations.

### Test Cases

| Test Case   | Validation |
|------------ |------------|
| Base Case   | PASS |
| Test Case 1 | PASS |
| Test Case 2 | PASS |
| Test Case 3 | PASS |
| Test Case 4 | PASS |
| Test Case 5 | PASS |
| Test Case 6 | PASS |
| Test Case 7 | PASS |
| Test Case 8 | PASS |
| Test Case 9 | PASS |
| Test Case 10| PASS |

For each test case, the program validates that the number of delivered packages matches the number of packages provided in the input.

All tested cases passed the delivery validation.

## Validation

The program includes an automatic delivery validation step.

Example:

Delivery validation:
Total packages: 5
Delivered packages: 5
Status: PASS


A 'PASS' status indicates that all input packages were successfully processed and delivered by the simulation.

## Input Normalization and Support

The program supports different JSON input structures by normalizing the data before processing.

For example:

- Warehouse data can be normalized from dictionary format to the internal list format.
- Agent data can be normalized from dictionary format to the internal list format.
- Package warehouse references using 'warehouse' can be normalized to 'warehouse_id'.

The main simulation then operates on the normalized structure.

## Limitations

The basic simulation does not model real-world delivery constraints such as:

- Traffic conditions
- Road networks
- Delivery time windows
- Vehicle capacity
- Weather conditions
- Package priorities
- Dynamic route optimization

The simulation uses coordinate-based Euclidean distance and the routing assumptions described above.

## Future Improvements

Possible future improvements include:

- Adding random delivery delays
- Generating ASCII-based delivery routes
- Supporting agents joining during the simulation
- Generating a CSV report for top-performing agents
- Adding more advanced route optimization
- Adding visualization of warehouses, agents, and delivery routes

## Conclusion

The Mystery Delivery System provides a simple Python simulation of a logistics delivery operation.

It demonstrates:

- JSON data handling
- Data normalization
- Euclidean distance calculation
- Nearest-agent assignment
- Delivery simulation
- Performance calculation
- Input validation
- JSON report generation

The system is designed to be simple, readable, and easy to test with different JSON inputs.
