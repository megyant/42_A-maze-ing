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
        self.pattern_cells: Set[Tuple[int, int]] = set()

    def ensure_valid_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        if pos in self.pattern_cells or not (0 <= x < self.width and
                                             0 <= y < self.height):
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in self.pattern_cells:
                        return (x, y)
            raise RuntimeError("No valid positions available in the maze.")
        return pos

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
                     (6, 1), (6, 2), (5, 2),
                     (4, 2), (4, 3), (4, 4),
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
            self.pattern_cells.add((target_x, target_y))

    def generate(self, start_pos: Tuple[int, int]) -> None:
        self.inject_42()
        start_pos = self.ensure_valid_position(start_pos)
        if start_pos in self.visited:
            start_pos = (0, 0)
        self.stack.append(start_pos)
        self.visited.add(start_pos)
        while self.stack:
            current_x, current_y = self.stack[-1]
            neighbors = self._get_unvisited_neighbors(current_x, current_y)
            if neighbors:
                next_x, next_y, direction = random.choice(neighbors)
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

    def make_imperfect(self, chance: float = 0.1) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.visited:
                    continue
                if random.random() < chance:
                    wall = random.choice([2, 4])
                    if wall == 2 and x < self.width - 1:
                        if (self.grid[y][x] & 2) and \
                                (x + 1, y) not in self.visited:
                            self.grid[y][x] &= ~2
                            self.grid[y][x+1] &= ~8
                    elif wall == 4 and y < self.height - 1:
                        if (self.grid[y][x] & 4) and \
                                (x, y + 1) not in self.visited:
                            self.grid[y][x] &= ~4
                            self.grid[y+1][x] &= ~1

    def display(
            self, path_str: str = "",
            start_pos: Tuple[int, int] = (0, 0),
            end_pos: Tuple[int, int] | None = None
            ) -> None:
        WHITE = "\033[97m"
        SPECIAL = "\033[91m"
        GREEN = "\033[92m"
        RED = "\033[91m"
        RESET = "\033[0m"
        path_coords = set()
        curr_x, curr_y = start_pos
        path_coords.add((curr_x, curr_y))
        for d in path_str:
            if d == "N":
                curr_y -= 1
            elif d == "S":
                curr_y += 1
            elif d == "E":
                curr_x += 1
            elif d == "W":
                curr_x -= 1
            path_coords.add((curr_x, curr_y))
        print(WHITE + "╔" + "═══╦" * (self.width - 1) + "═══╗" + RESET)
        for y in range(self.height):
            l1, l2 = "", ""
            border_c = SPECIAL if (0, y) in self.pattern_cells else WHITE
            l1 += border_c + "║" + RESET
            l2 += border_c + ("╠" if y < self.height - 1 else "╚") + RESET
            for x in range(self.width):
                is_42 = (x, y) in self.pattern_cells
                c = SPECIAL if is_42 else WHITE
                if (x, y) == start_pos:
                    content = f"{GREEN} S {RESET}"
                elif end_pos and (x, y) == end_pos:
                    content = f"{RED} E {RESET}"
                elif (x, y) in path_coords:
                    content = f"{c} ● {RESET}"
                else:
                    content = "   "
                if self.grid[y][x] & 2:
                    is_east_neighbor_42 = x < self.width - 1 and \
                        (x + 1, y) in self.pattern_cells
                    wall_color = (
                        SPECIAL if (is_42 or is_east_neighbor_42)
                        else WHITE
                    )
                    l1 += content + wall_color + "║" + RESET
                else:
                    l1 += content + " "
                if y < self.height - 1:
                    is_south_neighbor_42 = (x, y + 1) in self.pattern_cells
                    wall_s_color = (
                        SPECIAL if (is_42 or is_south_neighbor_42)
                        else WHITE
                    )
                    south_wall = "═══" if self.grid[y][x] & 4 else "   "
                    l2 += wall_s_color + south_wall + RESET
                    if x < self.width - 1:
                        is_corner_42 = any(
                            p in self.pattern_cells
                            for p in [(x, y),
                                      (x + 1, y),
                                      (x, y + 1),
                                      (x + 1, y + 1)]
                        )
                        l2 += (
                            SPECIAL if is_corner_42
                            else WHITE) + "╬" + RESET
                    else:
                        l2 += (SPECIAL if is_42 else WHITE) + "╣" + RESET
                else:
                    char = "╩" if x < self.width - 1 else "╝"
                    l2 += f"{WHITE}═══{char}{RESET}"
            print(l1)
            print(l2)
