# A-maze-ing

*This project has been created as a part of the 42 curriculum by <dtalapan>dtalapan, <mbotelho>mbotelho*

**GitHub Profiles**:
 - dtalapan: https://github.com/dtalapan
 - mbotelho: https://github.com/megyant

## Description

A-maze-ing is is a Python-based tool designed to explore the mechanics of procedural maze generation. By visualizing these algorithms, users can gain a deeper understanding of graph theory, stack-based recursion, and data encoding (such as bit-to-hexadecimal translation).

### Maze Generation Algorithms

While various methods exist to generate a maze, they differ significantly in their approach:  
  
**Kruskal's Algorithm**
  
This randomized approach treats the maze as a forest of trees. It starts with all cells separated by walls and repeatedly removes a wall between two cells, merging their respective trees until only one tree remains—the completed maze.  

**Prim's Algorithm**
  
Similar to Kruskal’s, this is a "greedy" algorithm. It starts at a single point and grows the maze outward by randomly selecting a wall that connects the existing maze to a cell not yet visited.    
  
**Recursive Backtracker**
  
This algorithm uses a depth-first search (DFS) approach. It carves a path through a grid of walled cells, pushing the current path onto a stack. When it hits a dead end, it "backtracks" through the stack to find the nearest cell with unvisited neighbors.  
  
We chose this algorithm because it was the most straightforward to implement for our first experience with maze generation.

### Bit-to-hexadecimal
  
As previously described, the Recursive Backtracker starts with a grid where every cell is fully enclosed by four walls. We can represent the state of these walls using a 4-bit binary system, where each bit acts as a toggle (flag) for a specific direction:
  
| **Direction** | **Bit** | **Value (Decimal)** |
| ----          | ----    | ----                |
| **North**     | 0001    | 1                   |
| **East**      | 0010    | 2                   |
| **South**     | 0100    | 4                   |
| **West**      | 1000    | 8                   |
  
A cell's value is the sum of its active wall bits. This allows us to store the entire state of a cell in a single nibble (4 bits). A cell with all four walls intact has a decimal value of 15 (1+2+4+8),represented in binary as 1111. When the algorithm "carves" a path, it subtracts the value of that wall. For example, if you remove the North wall from a closed cell, the new value becomes 14, represented in binary as 1110.  
  
This system is extremely useful since it maps perfectly to Hexadecimal, which means it becomes easier to store large informations of integers to string.  

### Breadth-first search (BFS)

BFS is a traversal algorithm that begins at the root node and systematically explores all neighboring nodes at the current depth before moving to the next level. This "layer-by-layer" approach is used to find the shortest path within a graph.  
  
Because the algorithm operates on the connectivity between nodes, it is highly versatile and can be applied to both undirected and directed graphs. In the context of maze solving, this ensures that the first time the exit is reached, the path taken is the most efficient one possible.  


## Instructions

### Installation

```
# Clone the repository
git@github.com:megyant/42_A-maze-ing.git a-maze-ing
cd a-maze-ing
```

```
# Install dependencies
make install
```

### Execution
```
# Run the maze generator
make run

# Run with a configuration file
python3 a_maze_ing.py config.txt

# Run checks (mypy and flake8)
make lint
```

### Structure of the Configuration File

```
# Mandatory
WIDTH=30                         # Maze width (number of cells) - must be > 0
HEIGHT=20                        # Maze height (number of cells) - must be > 0
ENTRY=1,1                        # Entry point coordinates (x, y)
EXIT=28,18                       # Exit point coordinates (x, y)
OUTPUT_FILE=output_maze.txt      # Output file
PERFECT=True                     # If enabled (True) maze will contain exactly one path. False to disable

# Optional
SEED=10                          # Number to initiate semi-random generation
```

### Maze Interaction

There are some available options to interact with the maze:
- m or --maze: generate a new maze
- p or --path: show/hide shortest path available
- c or --color: change maze color
- clear or --clear: clear maze
- q or --quit: exit configuration mode
  
## Code Reusability

For this project the class ```MazeGenerator``` available in the ```MazeGenerator.py``` file can be used as a standalone reusable component. It can be installed via pip:
  
//try to turn this into .gz and pip when completed
  
### Instatiate and use the generator

```
from MazeGenerator import MazeGenerator

generator = MazeGenerator(width=30, height=20, seed=10)

entry = (0, 0)
exit = (28, 18)

maze = maze.generate(start_pos=entry)
path = maze.find_path(start=entry, end=exit)

```
  
**Custom parameters:**
- width: maze width (number of cells) - int
- height: maze height (number of cells) - int
- seed: Number to initiate semi-random generation - int or None

**Access generated structure:**

Access width, height and seed:
```
maze.width
maze.height
maze.seed
```

Access grid:
```
maze.grid
```
// Any others?  
// BTW is perfect maze working? Its not tried but couldnt fix it  

## Resources
- [Jamisbuck's blog](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)  
- [Maze Generation Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)  
- [Fundamentals of Maze Generation](https://www.cs.cmu.edu/~112-n23/notes/student-tp-guides/Mazes.pdf)  
- [Invent with python](https://inventwithpython.com/recursion/chapter11.html)  
- [Stack Overflow](https://stackoverflow.com/questions/31326141/bitwise-logic-on-maze-walls)  
- [Assert not magic](https://www.assertnotmagic.com/2019/03/21/binary-operations/)  
- [Real Python](https://realpython.com/python-bitwise-operators/)  

### Use of Artificial Intelligence

Gemini V3 was used to optimize the development workflow in this project. Some usages include:
- Assist with the comprehension of bitwise translation
- Assist with the understanding of maze generation mathemaics
- Logical improvement of functions
- Makefile adjustments
- Improving this README wording

All algorithm and implementation are both authors' own work

## Team and project management

Our project was built on a foundation of clear communication and specialized roles. By dividing responsibilities based on individual strengths, we ensured a streamlined development process.

### Roles and Responsabilities

| **Team Member**           | **Primary Focus and Contributions** 
| ----                      | ----   
| **Denisa (dtalapan)**     | Core Engineering: Developed the maze generation logic, input parsing systems, and pathfinding algorithms.  
| **Margarida (mbotelho)**  | UX & Infrastructure: Designed the user interface, managed the project lifecycle (Makefile/README), and oversaw task delegation.  

### Development Workflow

The project followed a tiered implementation strategy. Initially, we collaborated to define the core maze logic and pathfinding requirements. Leveraging her experience with Python, Denisa developed the initial "skeleton" of the generation and traversal algorithms.

Following the architectural phase, we conducted a joint code review to optimize performance and ensure logic consistency. User interaction layers and infrastructure were then integrated. The final stage involved rigorous edge-case testing.

### Project Retrospective

 - **Efficient Task Allocation:** Defining clear expectations early on allowed both members to work in parallel without bottlenecks.
 - Algorithmic Integrity: The choice of algorithm allowed for a strict enforcement of maze rules.
 - User-Centric Design: The interface was designed to be intuitive, providing clear feedback during the generation and solving processes
 - Protections: The code is well-protected against invalid configurations and edge-case inputs.

 **What could be improved**
 - Render: Display is currently limited to ASCII characters.
 - Maze generation: Only one maze generation algorithm currently supported
 - Pathfinding: Only one pathfinding algorithm implemented
 - Animations: There are no real-time visual animations for the generation or solving processes.
