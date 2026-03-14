import random
from typing import Any, Dict, List, Tuple, Set, Optional
from collections import deque


class MazeGenerator:
    """ Provide tools to generate a maze using recursive
        backtracker algorithm.
    """
    def __init__(
            self,
            width: int,
            height: int,
            seed: Optional[int] = None) -> None:
        """
        Initialize the maze generator class.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
            seed: An optional integer to seed the random number generator.
        """
        full_grid = 15  # sum of bits representing each wall

        self.width: int = width
        self.height: int = height

        self.grid: List[List[int]] = [
            [full_grid for _ in range(width)]
            for _ in range(height)]  # initializing grid

        if seed is not None:  # if no seed, then randomly select one
            random.seed(seed)

        # cell being worked on
        self.stack: List[Tuple[int, int]] = []
        # set of cells that have been worked on
        self.visited: Set[Tuple[int, int]] = set()
        # cells belonging to 42 pattern
        self.pattern_cells: Set[Tuple[int, int]] = set()

        self.color: Dict[str, str] = {  # default maze colors
                            "MAIN": "\033[97m",   # Maze walls - white
                            "42": "\033[91m",     # 42 pattern - red
                            "START": "\033[92m",  # Start dot - green
                            "END": "\033[91m",    # End dot - red
                            "RESET": "\033[0m"}   # default terminal color

        self.injected = True  # has 42 pattern been inject
        # is the position valid (e.g. outsice of boundaries)
        self.valid_position = True

    def ensure_valid_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Check if a position is valid and return an alternative if not.

        A position is invalid if it lies outside of grid boundaries or
        whitin a reserved pattern (e.g. 42 pattern).

        Args:
            pos: A tuple representing coordinates (x, y) to check.

        Returns:
            The original position if valid or the first available valid cell.
        """
        x, y = pos  # unpacking the Tuple in the two points of a coordinate
        # if in 42 pattern or outside maze boundaries
        if pos in self.pattern_cells or not (0 <= x < self.width and
                                             0 <= y < self.height):
            self.valid_position = False  # set valid position as false
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in self.pattern_cells:
                        # find next available point
                        return (x, y)
            raise RuntimeError("No valid positions available in the maze.")
        return pos

    def _get_unvisited_neighbors(self, x: int,
                                 y: int) -> List[Tuple[int, int, str]]:
        """
        Identify adjacent cells that have not yet been visited.

        Args:
            x: the x-coordinate.
            y: the y-coordinate

        Returns:
            A list of tuples containing(neighbor x, neighbor y, direction.
        """
        neighbors: List[Tuple[int, int, str]] = []   # create neigbors list

        if y > 0 and (x, y - 1) not in self.visited:
            neighbors.append((x, y - 1, "N"))        # append north cell

        if y < self.height - 1 and (x, y + 1) not in self.visited:
            neighbors.append((x, y + 1, "S"))        # append south cell

        if x > 0 and (x - 1, y) not in self.visited:
            neighbors.append((x - 1, y, "W"))        # append west cell

        if x < self.width - 1 and (x + 1, y) not in self.visited:
            neighbors.append((x + 1, y, "E"))        # append east cell

        return neighbors

    def inject_42(self) -> None:
        """
        Carve a 42 patern into the center of the maze.

        Reseves specific cells and prevents them from
        being a part of the maze-generation process.
        """
        # 7x5 area for 42
        # 4 is 3x5

        ft_width = 7   # 42 width
        ft_height = 5  # 42 height
        full_grid = 15  # sum of bits representing each wall

        self.injected = True

        pattern_4 = [(0, 0), (0, 1), (0, 2),
                     (1, 2), (2, 0), (2, 1),
                     (2, 2), (2, 3), (2, 4)]  # 4 form

        pattern_2 = [(4, 0), (5, 0), (6, 0),
                     (6, 1), (6, 2), (5, 2),
                     (4, 2), (4, 3), (4, 4),
                     (5, 4), (6, 4)]          # 2 form

        all_42 = pattern_4 + pattern_2        # 42 form

        if self.width < 10 or self.height < 7:
            raise ValueError("Error: Maze size too small to display full '42'"
                             "pattern")  # check if maze is bigger than 42

        # Cells available after 42 injection
        start_x = (self.width - ft_width) // 2
        # Cells available after 42 injection
        start_y = (self.height - ft_height) // 2

        for offset_x, offset_y in all_42:
            target_x = start_x + offset_x  # absolute horizontal position
            target_y = start_y + offset_y  # absolute vertical position

            # reset cell to full wall
            self.grid[target_y][target_x] = full_grid
            # mark cell as visited
            self.visited.add((target_x, target_y))
            # add cell to pattern cells list
            self.pattern_cells.add((target_x, target_y))

    def generate(self, start_pos: Tuple[int, int]) -> None:
        """
        Carve the  maze paths using a recursive
        backtracker agorithm.

        Args:
            start_pos: The (x, y) coordinates where
            the generation starts.
        """
        # Attempts to inject 42 pattern, if not possible retuns a error message
        try:
            self.inject_42()
        except ValueError:
            self.injected = False  # toggle injected to false
            print("Error: Maze size too small to display full '42'pattern")

        # ensure start is in a valid position
        start_pos = self.ensure_valid_position(start_pos)

        # if position in visited, then default is (0, 0)
        if start_pos in self.visited:
            start_pos = (0, 0)

        self.stack.append(start_pos)  # add position to stack
        self.visited.add(start_pos)   # add position to visited

        while self.stack:
            # get current location
            current_x, current_y = self.stack[-1]
            # get unvisited cells
            neighbors = self._get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                # select one valid neighbor
                next_x, next_y, direction = random.choice(neighbors)
                if direction == "N":
                    # remove north wall
                    self.grid[current_y][current_x] -= 1
                    # remove neighbor south wall
                    self.grid[next_y][next_x] -= 4

                elif direction == "S":
                    # remove south wall
                    self.grid[current_y][current_x] -= 4
                    # remove neighbor north wall
                    self.grid[next_y][next_x] -= 1

                elif direction == "E":
                    # remove east wall
                    self.grid[current_y][current_x] -= 2
                    # remove neighbor west wall
                    self.grid[next_y][next_x] -= 8

                elif direction == "W":
                    # remove west wall
                    self.grid[current_y][current_x] -= 8
                    # remove neighbor east wall
                    self.grid[next_y][next_x] -= 2

                self.visited.add((next_x, next_y))
                self.stack.append((next_x, next_y))
            else:
                # if no path found pop the last location and backtrack
                self.stack.pop()

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        """
        Find the shortest path between two points using Breadth-First Search.

        Args:
            start: coordinates to the start of the search.
            end:  coordinates of the target destination.

        Returns:
            A string of directional characters.
        """
        # initialize queue with start position
        queue = deque([start])

        # dictionary to store the trail
        parent: Dict[Tuple[int, int], Any] = {}
        parent[start] = None
        path_list: List[str] = []

        while queue:
            # pop the oldest discovered node
            current = queue.popleft()

            # if goal is reached stop searching
            if current == end:
                break

            x, y = current

            # get the current cell grid
            val = self.grid[y][x]

            north_bit = 1
            east_bit = 2
            south_bit = 4
            west_bit = 8

            # map potential movements
            directions = [
                    ((x, y - 1), "N", north_bit),
                    ((x + 1, y), "E", east_bit),
                    ((x, y + 1), "S", south_bit),
                    ((x - 1, y), "W", west_bit),
            ]

            # if the wall is open, check if neighbor is unvisited
            for neighbor, char, bit in directions:
                if not (val & bit) and neighbor not in parent:
                    # record path
                    parent[neighbor] = (current, char)
                    queue.append(neighbor)

        current = end
        # trace backwards from end to start using parent map
        while current != start and current in parent:
            entry = parent[current]
            if entry is not None:
                current_node, char = entry
                path_list.append(char)  # store direction
                current = current_node  # move to the parent node
            else:
                break

        # return string in reverse order to have correct path list
        return "".join(reversed(path_list))

    def make_imperfect(self, chance: float = 0.4) -> None:
        """
        Convert perfect maze into imperfect by removing random walls.

        Args:
            chance: float between 0 and 1 representing the probability of
                    attempring to break a wall.
        """
        walls_broken = 0  # debug variable to confirm it's working

        for y in range(self.height):
            for x in range(self.width):
                # skip cells protected by 42 pattern
                if (x, y) in self.pattern_cells:
                    continue

                if random.random() < chance:
                    # Randomly choose to break east or south wall
                    wall = random.choice([2, 4])

                    # breaking east wall
                    if wall == 2 and x < self.width - 1:

                        if (x + 1, y) not in self.pattern_cells:
                            # check for 3x3 pattern
                            gap_up = (y > 0) and not (self.grid[y-1][x] & 2)
                            gap_down = ((y < self.height - 1)
                                        and not (self.grid[y+1][x] & 2))
                            three_pattern = gap_up and gap_down

                            if not three_pattern and (self.grid[y][x] & 2):
                                # turn this bit off without touching others
                                self.grid[y][x] &= ~2
                                # turn this bit off without touching others
                                self.grid[y][x+1] &= ~8
                                walls_broken += 1

                    # breaking south wall
                    elif wall == 4 and y < self.height - 1:

                        if (x, y + 1) not in self.pattern_cells:
                            # check for 3x3 pattern
                            gap_up = (x > 0) and not (self.grid[y][x-1] & 4)
                            gap_down = ((x < self.width - 1)
                                        and not (self.grid[y][x+1] & 4))
                            three_pattern = gap_up and gap_down

                            if not three_pattern and (self.grid[y][x] & 2):
                                # turn this bit off without touching others
                                self.grid[y][x] &= ~4
                                # turn this bit off without touching others
                                self.grid[y+1][x] &= ~1
                                walls_broken += 1

    def display(
            self, path_str: str = "",
            color: Dict[str, str] | None = None,
            start_pos: Tuple[int, int] = (0, 0),
            end_pos: Tuple[int, int] | None = None
            ) -> None:
        """
        Render the maze to the terminal using Unicode
        box-drawing characters.

        Args:
            path_str: A string of directions.
            color: Optional dictionary of ANSI color codes.
            start_pos: Coordinates for the start.
            end_pos: coordinates for end
        """
        # if no other color provived use default defined
        color = color if color is not None else self.color

        path_coords = set()

        curr_x, curr_y = start_pos

        # convert string into a set
        if path_str:
            path_coords.add((curr_x, curr_y))
        for char in path_str:
            if char == "N":
                curr_y -= 1
            elif char == "S":
                curr_y += 1
            elif char == "E":
                curr_x += 1
            elif char == "W":
                curr_x -= 1
            path_coords.add((curr_x, curr_y))

        # top boundary
        print(
            color.get("MAIN", "") +
            "╔" + ("═══╦" * (self.width - 1)) + "═══╗" +
            color.get("RESET", "")
        )

        for y in range(self.height):
            # l1 hold vertical walls
            # l2 holds bottom walls
            l1, l2 = "", ""

            # determine color for the leftmost border wall
            border_c = (color.get("42") if (0, y) in self.pattern_cells
                        else color.get("MAIN"))
            l1 += f"{border_c}║{color.get('RESET', '')}"

            # choose correct joint character
            joint = "╠" if y < self.height - 1 else "╚"
            l2 += (
                f"{border_c or ''}"
                f"{joint}"
                f"{color.get('RESET', '')}"
            )

            for x in range(self.width):
                is_42 = (x, y) in self.pattern_cells
                c = color.get("42") if is_42 else color.get("MAIN")

                # determine cell content
                if end_pos and (x, y) == end_pos:
                    content = f"{color.get("START")} ⦿ {color.get("RESET")}"
                elif (x, y) == start_pos:
                    content = f"{color.get("END")} ⦿ {color.get("RESET")}"
                elif (x, y) in path_coords:
                    content = f"{c} ● {color.get("RESET")}"
                else:
                    content = "   "

                # handle vertical (east) walls
                if self.grid[y][x] & 2:
                    # color if neighbor is part of the 42 patter
                    is_east_neighbor_42 = x < self.width - 1 and \
                        (x + 1, y) in self.pattern_cells
                    wall_color = (
                        color.get("42") if (is_42 or is_east_neighbor_42)
                        else color.get("MAIN")
                    )
                    reset = color.get("RESET", "")
                    wall = wall_color or ""
                    l1 += f"{content}{wall}║{reset}"
                else:
                    l1 += content + " "

                # handle horizontal (south) walls
                if y < self.height - 1:
                    is_south_neighbor_42 = (x, y + 1) in self.pattern_cells
                    wall_s_color = (
                        color.get("42") if (is_42 or is_south_neighbor_42)
                        else color.get("MAIN")
                    )

                    # dram solid if bit 4 else draw space
                    south_wall = "═══" if self.grid[y][x] & 4 else "   "
                    w_color = wall_s_color or ""
                    reset = color.get("RESET", "")
                    l2 += f"{w_color}{south_wall}{reset}"

                    # determine intersection
                    if x < self.width - 1:
                        is_corner_42 = any(
                            p in self.pattern_cells
                            for p in [(x, y),
                                      (x + 1, y),
                                      (x, y + 1),
                                      (x + 1, y + 1)]
                        )
                        l2 += (
                            color.get("42", "") if is_corner_42
                            else color.get("MAIN", "")
                        ) + "╬" + color.get("RESET", "")

                    else:
                        l2 += (
                            color.get("42", "") if is_42
                            else color.get("MAIN", "")
                        ) + "╣" + color.get("RESET", "")

                else:
                    # dram final bottom boundary
                    char = "╩" if x < self.width - 1 else "╝"
                    l2 += f"{color.get("MAIN")}═══{char}{color.get("RESET")}"

            # print lines
            print(l1)
            print(l2)


class Maze(MazeGenerator):
    """ Manage construction and structural properties of maze """
    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None, perfect: bool = True) -> None:
        """
        Initialize maze structure.

        Args:
            width: horizontal size of the maze.
            height: vertical size of the maze.
            seed: seed for random number generation.
            perfect: boolean to determine if maze should be perfect.
        """
        super().__init__(width, height, seed)
        self.perfect = perfect

    def build(self, start_pos: Tuple[int, int] = (0, 0)) -> None:
        """
        Execute full maze construction process.

        Args:
            start_pos: the coordinates to begin path carving
        """

        full_grid = 15

        self. grid = [[full_grid for _ in range(self.width)]
                      for _ in range(self.height)]

        self.visited = set()
        self.stack = []

        self.generate(start_pos=start_pos)

        if not self.perfect:
            self.make_imperfect(chance=0.4)

        self.generated = True


class Display_Maze(Maze):
    """
    User interface layer for rendering the maze with different
    visual modes.
    """
    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None, perfect: bool = True) -> None:
        """ Initialize settings """
        super().__init__(width, height, seed, perfect)
        # show/hide solution path
        self.show_path = False
        # switch between default and neon color palette
        self.color_change = False

    def render(
        self,
        path_str: str = "",
        start_pos: Tuple[int, int] = (0, 0),
        end_pos: Optional[Tuple[int, int]] = None
    ) -> None:
        """
        Prepare and print maze visualization.

        Args:
            path_str: the direction string.
            start_pos: start coordinates
            end_pos: end coordinates
        """
        # only show path if activates
        active_path = path_str if self.show_path else ""

        # neon palette
        active_colors = None
        if self.color_change is True:
            active_colors = {
                "MAIN": "\033[95m",
                "42": "\033[96m",
                "START": "\033[94m",
                "END": "\033[93m",
                "RESET": "\033[0m"
            }

        # display maze
        self.display(path_str=active_path, color=active_colors,
                     start_pos=start_pos, end_pos=end_pos)
