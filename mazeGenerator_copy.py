import random
from typing import Any, Dict, List, Tuple, Set, Optional
from collections import deque


class MazeGenerator:
    def __init__(
            self,
            width: int,
            height: int,
            seed: Optional[int] = None
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: List[List[int]] = [
            [15 for _ in range(width)]  # magic number 15
            for _ in range(height)]

        if seed is not None:
            random.seed(seed)

        self.stack: List[Tuple[int, int]] = []
        self.visited: Set[Tuple[int, int]] = set()

    def _get_unvisited_neighbors(self, x: int,
                                 y: int) -> List[Tuple[int, int, str]]:

        neighbors: List[Tuple[int, int, str]] = []

        if y > 0 and (x, y - 1) not in self.visited:
            neighbors.append((x, y - 1, "N"))
        if y < self.height - 1 and (x, y + 1) not in self.visited:
            neighbors.append((x, y + 1, "S"))
        if x > 0 and (x - 1, y) not in self.visited:
            neighbors.append((x - 1, y, "W"))
        if x < self.width - 1 and (x + 1, y) not in self.visited:
            neighbors.append((x + 1, y, "E"))

        return neighbors

    def inject_42(self) -> None:
        # 7x5 area for 42
        # 4 is 3x5
        pattern_4 = [(0, 0), (0, 1), (0, 2),
                     (1, 2), (2, 0), (2, 1),
                     (2, 2), (2, 3), (2, 4)]

        pattern_2 = [(4, 0), (5, 0), (6, 0),
                     (6, 1), (6, 2),
                     (5, 2), (4, 2),
                     (4, 3), (4, 4),
                     (5, 4), (6, 4)]

        all_42 = pattern_4 + pattern_2

        if self.width < 10 or self.height < 7:
            raise ValueError("Error: Maze size too small to display full '42'"
                             "pattern")  # ValueError instead of just print

        start_x = (self.width - 7) // 2  # Magic Number 7
        start_y = (self.height - 5) // 2  # Magic number 5

        for dx, dy in all_42:
            target_x = start_x + dx  # Name dx and dy could be more clear
            target_y = start_y + dy

            self.grid[target_y][target_x] = 15  # Magic Number 15

            self.visited.add((target_x, target_y))

    def generate(self, start_pos: Tuple[int, int]) -> None:

        self.inject_42()

        if start_pos in self.visited:
            start_pos = (0, 0)

        self.stack.append(start_pos)
        self.visited.add(start_pos)

        while self.stack:
            current_x, current_y = self.stack[-1]
            neighbors = self._get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                next_x, next_y, direction = random.choice(neighbors)
                # Magic numbers below:
                if direction == "N":
                    self.grid[current_y][current_x] -= 1
                    self.grid[next_y][next_x] -= 4

                elif direction == "S":
                    self.grid[current_y][current_x] -= 4
                    self.grid[next_y][next_x] -= 1

                elif direction == "E":
                    self.grid[current_y][current_x] -= 2
                    self.grid[next_y][next_x] -= 8

                elif direction == "W":
                    self.grid[current_y][current_x] -= 8
                    self.grid[next_y][next_x] -= 2

                self.visited.add((next_x, next_y))
                self.stack.append((next_x, next_y))

            else:
                self.stack.pop()

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:

        queue = deque([start])
        parent: Dict[Tuple[int, int], Any] = {}
        parent[start] = None
        path_list: List[str] = []  # Moved up

        while queue:
            current = queue.popleft()  # Changed curr to current
            if current == end:
                break

            x, y = current

            val = self.grid[y][x]

            # Magic Numbers:
            directions = [
                    ((x, y - 1), "N", 1),
                    ((x + 1, y), "E", 2),
                    ((x, y + 1), "S", 4),
                    ((x - 1, y), "W", 8),
            ]

            for neighbor, char, bit in directions:

                if not (val & bit) and neighbor not in parent:
                    parent[neighbor] = (current, char)
                    queue.append(neighbor)

        current = end

        while current != start and current in parent:
            entry = parent[current]
            if entry is not None:
                current_node, char = entry
                path_list.append(char)
                current = current_node
            else:
                break

        return "".join(reversed(path_list))

# MADE BY AI DELETE LATER JUST TO CHECK HOW TO MAKE ASCII ART
    def display(self, path_str: str = "", start_pos: Tuple[int, int] = (0, 0)) -> None:
        # 1. Convert the path string into a set of (x, y) coordinates for quick lookup
        path_coords = set()
        if path_str:
            curr_x, curr_y = start_pos
            path_coords.add((curr_x, curr_y))
            for direction in path_str:
                if direction == "N": curr_y -= 1
                elif direction == "S": curr_y += 1
                elif direction == "E": curr_x += 1
                elif direction == "W": curr_x -= 1
                path_coords.add((curr_x, curr_y))

        # 2. Draw the maze
        print("+" + "---+" * self.width)
        for y in range(self.height):
            line1 = "|"
            line2 = "+"
            for x in range(self.width):
                val = self.grid[y][x]

                # Decide what character to put in the cell body
                # If the coordinate is in our path set, use a dot '.', otherwise a space ' '
                cell_content = " . " if (x, y) in path_coords else "   "

                # Check East Wall (bit 2)
                if val & 2:
                    line1 += cell_content + "|"
                else:
                    line1 += cell_content + " "

                # Check South Wall (bit 4)
                if val & 4:
                    line2 += "---+"
                else:
                    line2 += "   +"
            print(line1)
            print(line2)


class Maze(MazeGenerator):
    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None) -> None:
        super().__init__(width, height, seed)
        self.wall_color = "white"

    def build(self):
        self. grid = [[15 for _ in range(self.width)]  # magic number 15
                      for _ in range(self.height)]
        self.visited = set()
        self.stack = []

        self.generate((0, 0))
        self.generated = True


class Display_Maze(Maze):

    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None) -> None:
        super().__init__(width, height)
        self.show_path = False

    def render(self, path_str: str = "", start_pos: Tuple[int, int] = (0, 0)):
        self.display(path_str=path_str, start_pos=start_pos)


