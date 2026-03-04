import sys
from typing import Dict, Any, Tuple
from mazeGenerator import MazeGenerator


def check_mandatory_keys(config: Dict[str, Any]) -> None:
    try:
        mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"]

        for key in mandatory:
            if key not in config:
                raise ValueError("Error: Missing mandatory configuration "
                                 f"key: {key}.")

    except ValueError as e:
        print(e)
        sys.exit(1)


def parse_config(file_path: str) -> Dict[str, Any]:
    config: Dict[str, Any] = {}

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ValueError("Error: Invalid syntax on line "
                                     f"{line_num}: '{line}'.")
                # Changed print to ValueError

                key, value = line.split('=', 1)
                config[key.strip().upper()] = value.strip()

        check_mandatory_keys(config)
        return config

    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        sys.exit(1)

    except ValueError as e:
        print(e)
        sys.exit(1)

    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def format_cords(coord_Str: str) -> Tuple[int, int]:
    try:
        x, y = map(int, coord_Str.split(','))
        return (x, y)
    except ValueError:
        print(f"Error: Invalid coordinate format '{coord_Str}'. Use 'x,y'.")
        sys.exit(1)


def main() -> None:
    try:  # try for the int()
        config = parse_config("config.txt")

        # Magic Numbers
        width = int(config.get("WIDTH", 10))
        height = int(config.get("HEIGHT", 10))

        entry = format_cords(config.get("ENTRY", "0,0"))
        # Changed exit_p to exit_point and out_file to output_file
        exit_point = format_cords(config.get("EXIT",
                                             f"{width - 1}, {height - 1}"))
        output_file = config.get("OUTPUT_FILE", "output_maze.txt")
        seed = int(config["SEED"]) if "SEED" in config else None

        # maybe create a custom error and add OR instead of if if
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            print("Error: ENTRY point is out of maze bounds")
            sys.exit(1)
        if not (0 <= exit_point[0] < width and 0 <= exit_point[1] < height):
            print("Error: EXIT point is out of maze bounds")
            sys.exit(1)

        gen = MazeGenerator(width, height, seed=seed)
        gen.generate(entry)

        # MADE BY AI DELETE AFTER
        print("\nGenerated Maze:")
        gen.display()

        path_str = gen.find_path(entry, exit_point)

    except Exception:
        print("Error: An unexpected error occurred")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    try:
        with open(output_file, 'w') as f:
            for row in gen.grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_point[0]},{exit_point[1]}\n")
            f.write(path_str + "\n")

        print(f"Maze sucessfully saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
