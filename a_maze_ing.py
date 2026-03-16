import sys
from typing import Dict, Any, Tuple
from MazeGenerator import Display_Maze


def check_mandatory_keys(config: Dict[str, str]) -> None:
    """
    Verify that all required configuration keys are present.

    Args:
        config: the dictionary of settings parsed.
    """
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
    """
    Read and parse a configuration file into a dictionary.

    Args:
        file_path: the path to the txt configuration path.

    Returns:
        A dictionary containg key-value pairs from the file.
    """
    config: Dict[str, Any] = {}

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # skip empty lines
                if not line or line.startswith('#'):
                    continue
                # ensure it follows kew=value format
                if '=' not in line:
                    raise ValueError("Error: Invalid syntax on line "
                                     f"{line_num}: '{line}'.")
                key, value = line.split('=', 1)
                config[key.strip().upper()] = value.strip()

        # validate dictionary
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
        sys.exit(1)


def format_cords(coord_Str: str) -> Tuple[int, int]:
    """ Converts a comma-separated strinf into a tuple (x, y). """
    try:
        x, y = map(int, coord_Str.split(','))
        return (x, y)

    except ValueError:
        print(f"Error: Invalid coordinate format '{coord_Str}'. Use 'x,y'.")
        sys.exit(1)


def user_input(maze: "Display_Maze", path: str, config: Dict[str, Any],
               start_pos: Tuple[int, int]) -> None:
    """ Run an interactive command-line loop. """
    width = int(config.get("WIDTH", 10))
    height = int(config.get("HEIGHT", 10))
    exit_point = format_cords(config.get("EXIT", f"{width - 1}, {height - 1}"))
    maze.perfect = maze.perfect

    try:
        prompt_lines = False
        # clear terminal and move cursor to home position
        print("\033[2J\033[H", end="", flush=True)

        while True:
            prompt = ("Available options:\n"
                      " . m or --maze: generate a new maze\n"
                      " . p or --path: show/hide shortest path available\n"
                      " . c or --color: change maze color\n"
                      " . clear or --clear: clear maze\n"
                      " . per or --perfect: toggle perfection\n"
                      " . q or --quit: exit configuration mode\n"
                      " command: ")

            command = input(f"\n{prompt}").strip().lower()

            if command == 'q' or command == '--quit':
                break

            elif command == 'm' or command == '--maze':
                # rebuild the maze with current settings
                maze.build()
                current_path = maze.find_path(start=start_pos, end=exit_point)
                print("\033[2J\033[H", end="", flush=True)

                # report maze generation errors
                if maze.injected is False:
                    print("Error: Maze size too small to display full '42'"
                          "pattern")
                if maze.valid_position is False:
                    print("Error: Not a valid position.")
                    break

                maze.render(end_pos=exit_point, start_pos=start_pos)
                maze.show_path = False
                prompt_lines = False

            elif command == 'p' or command == '--path':
                print("\033[2J\033[H", end="", flush=True)

                maze.show_path = not maze.show_path
                maze.render(path_str=current_path, end_pos=exit_point,
                            start_pos=start_pos)

                prompt_lines = False

            elif command == 'per' or command == '--perfect':
                print("\033[2J\033[H", end="", flush=True)

                print(f"Please create a new maze. Perfect = {maze.perfect}")
                if maze.perfect:
                    maze.perfect = False
                else:
                    maze.perfect = True

            elif command == 'c' or command == '--color':
                print("\033[2J\033[H", end="", flush=True)

                maze.color_change = not maze.color_change
                maze.render(path_str=current_path,
                            start_pos=start_pos,
                            end_pos=exit_point)

                prompt_lines = False

            elif command == 'clear' or command == '--clear':
                print("\033[2J\033[H", end="", flush=True)
                prompt_lines = False

            else:
                # handle ANSI cursor movement to overwrite
                # invalid input lines
                if prompt_lines is True:
                    print("\033[11A\r\033[J", end="")
                elif prompt_lines is False:
                    print("\033[9A\r\033[J", end="")
                    prompt_lines = True
                print("\nInvalid command. Try again")
                continue

    except Exception as e:
        print(f"oops something went wrong: {e}")


def main() -> None:
    """ Organize maze application. """
    try:
        # Parsing
        config = parse_config("config.txt")
        width = int(config.get("WIDTH", 10))
        height = int(config.get("HEIGHT", 10))

        config.get("OUTPUT_FILE", "output_maze.txt")

        seed = int(config["SEED"]) if "SEED" in config else None

        is_perfect = config.get("PERFECT", "TRUE").upper() == "TRUE"

        entry = format_cords(config.get("ENTRY", "0,0"))
        exit_point = format_cords(config.get("EXIT",
                                  f"{width - 1},{height - 1}"))

        # entry needs to be different from exit
        if entry == exit_point:
            print("Error: Entry Point and Exit Point cannot be the same.")
            sys.exit(1)

        # create maze object
        gen = Display_Maze(width=width, height=height, seed=seed,
                           perfect=is_perfect)

        # ensure entry and exit are valid
        entry = gen.ensure_valid_position(entry)
        exit_point = gen.ensure_valid_position(exit_point)

        # generate maze
        gen.generate(entry)

        #  make impefect if necessary
        if not is_perfect:
            gen.make_imperfect(chance=0.4)

        # find path
        path_str = gen.find_path(entry, exit_point)

        # initialize user interface
        try:
            user_input(gen, path_str, config, entry)
        except KeyboardInterrupt:
            print("Error: You left user interface.")

    except (Exception, ValueError) as e:
        print(f"Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
