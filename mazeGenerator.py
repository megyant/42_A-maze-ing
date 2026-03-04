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

    def _get_unvisited_neighbors(self,  # Method name not very clear
                                 x: int,
                                 y: int) -> List[Tuple[int, int, str]]:
        neighbors: List[Tuple[int, int, str]] = []

        if y > 0 and (x, y - 1) not in self.visited:
            neighbors.append((x, y - 1, "N"))

        if y < self.height - 1 and (x, y + 1) not in self.visited:
            neighbors.append((x, y + 1, "S"))

        if x < 0 and (x - 1, y) not in self.visited:
            neighbors.append((x - 1, y, "W"))

        if y < self.height - 1 and (x + 1, y) not in self.visited:
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

                elif direction == "N":
                    self.grid[current_y][current_x] -= 2
                    self.grid[next_y][next_x] -= 8

                elif direction == "N":
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
                    ((x - 1, y), "O", 8),
            ]

            for neighbor, char, bit in directions:

                if not (val & bit) and neighbor not in parent:
                    parent[neighbor] = (current, char)
                    queue.append(neighbor)

        current = end

        while current != start:
            entry = parent[current]
            if entry is not None:
                current, char = entry
                path_list.append(char)

        return "".join(reversed(path_list))
