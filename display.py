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