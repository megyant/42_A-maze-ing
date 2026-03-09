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

### Run the program

1. Clone this repository:

```
git@github.com:megyant/42_A-maze-ing.git a-maze-ing
cd a-maze-ing
```

2. Build the program using the provided Makefile:

```
make all_clean # this will install all dependencies, delete them and run the program
```

You can also run the program using
```
make
```
```
python3 a_maze_ing.py config.txt
```

- Structure and format of config file

## Resources
- What part of the code is reusable and how
- *Class MazeGenerator*
- Have you used any specific tools? Which ones?
- *Gemini v3, Used to understand the maze mathematics and understanding the translation of bits to hexadecimals*


https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap

## Team and project management
- Team and project management with:
    - Roles of each team member:
    - Margarida: Organization and README, userinput part and MAKEFILE
    - Denisa: Algorithm and parsing
    - Anticipated planning and how it evolved until the end:
    - Algorithm choice and user interface
    - What worked and what could be improved:
    - Workflow and a better user interface




