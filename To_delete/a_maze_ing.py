import sys
import random
from typing import Dict, Any, Tuple
from MazeGenerator import MazeGenerator


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
    try:
        config = parse_config("config.txt")
        width = int(config.get("WIDTH", 10))
        height = int(config.get("HEIGHT", 10))
        output_file = config.get("OUTPUT_FILE", "output_maze.txt")
        seed = int(config["SEED"]) if "SEED" in config else None
        is_perfect = config.get("PERFECT", "TRUE").upper() == "TRUE"
        if is_perfect:
            entry = format_cords(config.get("ENTRY", "0,0"))
            exit_point = format_cords(config.get("EXIT",
                                                 f"{width - 1},{height - 1}"))
        else:
            entry = (random.randint(0, width - 1),
                     random.randint(0, height - 1))
            exit_point = (random.randint(0, width - 1),
                          random.randint(0, height - 1))
            while exit_point == entry:
                exit_point = (random.randint(0, width - 1),
                              random.randint(0, height - 1))
        gen = MazeGenerator(width, height, seed=seed)
        entry = gen.ensure_valid_position(entry)
        exit_point = gen.ensure_valid_position(exit_point)
        print(f"Before generate: Entry -> {entry}, Exit -> {exit_point}")
        gen.generate(entry)
        entry = gen.ensure_valid_position(entry)
        exit_point = gen.ensure_valid_position(exit_point)
        print(f"After generate: Entry -> {entry}, Exit -> {exit_point}")
        if not is_perfect:
            gen.make_imperfect(chance=0.1)
        path_str = gen.find_path(entry, exit_point)
        print("\nVisualizing Maze with Path:")
        gen.display(path_str=path_str, start_pos=entry, end_pos=exit_point)
        with open(output_file, 'w') as f:
            for row in gen.grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_point[0]},{exit_point[1]}\n")
            f.write(path_str + "\n")
        print(f"Maze successfully saved to {output_file}")

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
