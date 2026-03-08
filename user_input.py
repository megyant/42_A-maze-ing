from mazeGenerator_copy import Display_Maze
from a_maze_ing import parse_config, format_cords
from typing import Tuple


def main() -> None:
    config = parse_config("config.txt")
    w = int(config.get("WIDTH", 10))
    h = int(config.get("HEIGHT", 10))

    entry = format_cords(config.get("ENTRY", "0,0"))
    exit_point = format_cords(config.get("EXIT",
                                         f"{w - 1}, {h - 1}"))

    maze = Display_Maze(width=w, height=h)
    maze.build()
    path_str = maze.find_path(entry, exit_point)

    print("\033[2J\033[H", end="", flush=True)

    if input("start version 1? ").lower() == "y":

        print("\n=== Version 1 ===\n")
        version1(maze, path_str, config)
    else:
        exit

    print("\033[2J\033[H", end="", flush=True)

    if input("start version 2? ").lower() == "y":
        print("\n=== Version 2 ===\n")

        maze.build()
        maze.render()
        rui_alexandre_version(maze, path_str, config)

    else:
        exit

    print("\033[2J\033[H", end="", flush=True)

    if input("start version 3? ").lower() == "y":
        print("\n=== Version 3 ===\n")

        maze.build()
        maze.render()
        version3(maze, path_str, config)
    else:
        exit


def version1(maze: Display_Maze, path: str, config: str,
             start_pos: Tuple[int, int] = (0, 0)) -> None:

    width = int(config.get("WIDTH", 10))
    height = int(config.get("HEIGHT", 10))
    exit_point = format_cords(config.get("EXIT", f"{width - 1}, {height - 1}"))

    current_path = path

    try:
        while True:

            while True:
                new_maze = input("\nCreate a new maze? (y/n/q): ").lower()

                if new_maze == 'y':
                    maze.build()
                    current_path = maze.find_path(start=start_pos,
                                                  end=exit_point)
                    print("\033[2J\033[H", end="", flush=True)
                    print("\n=== Version 1 ===\n")
                    maze.render()
                    break
                elif new_maze == 'n':
                    break
                elif new_maze == 'q':
                    break
                else:
                    print("Invalid option. Try Again.")
                    continue

            while True:
                path = input("\nShow/unshow shortest path available? "
                             "(p/continue/q): ").lower()

                if path == 'p':
                    print("\033[2J\033[H", end="", flush=True)
                    print("\n=== Version 1 ===\n")
                    if maze.show_path is False:
                        maze.render(path_str=current_path, start_pos=start_pos)
                        maze.show_path = True
                    elif maze.show_path is True:
                        maze.render()
                        maze.show_path = False
                elif path == 'continue':
                    break
                elif path == 'q':
                    break
                else:
                    print("Invalid command. Try Again.")
                    continue

            while True:
                color = input("\nChange maze color? (y/n/q): ").lower()

                if color == 'y':
                    maze.wall_color = "example"
                    print("\033[2J\033[H", end="", flush=True)
                    print("\n=== Version 2 ===\n")
                    maze.render()
                    print("Color changed")
                    break
                elif color == 'n':
                    break
                elif color == 'q':
                    break
                else:
                    print("Invalid command. Try Again.")
                    continue

            if new_maze == 'q' or path == 'q' or color == 'q':
                break
            else:
                continue
    except Exception as e:
        print(f"oops something went wrong: {e}")


def rui_alexandre_version(maze: Display_Maze, path: str, config: str,
                          start_pos: Tuple[int, int] = (0, 0)) -> None:

    width = int(config.get("WIDTH", 10))
    height = int(config.get("HEIGHT", 10))
    exit_point = format_cords(config.get("EXIT", f"{width - 1}, {height - 1}"))

    current_path = path

    try:
        while True:

            prompt = "(r)egenerate, (p)ath, (c)olor, (q)uit: "
            command = input(f"\n{prompt}").strip().lower()

            if command == 'q':
                break

            elif command == 'r':
                maze.build()
                current_path = maze.find_path(start=start_pos, end=exit_point)
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 2 ===\n")
                maze.render()

            elif command == 'p':
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 2 ===\n")
                if maze.show_path is False:
                    maze.render(path_str=current_path, start_pos=start_pos)
                    maze.show_path = True
                elif maze.show_path is True:
                    maze.render()
                    maze.show_path = False

            elif command == 'c':
                maze.wall_color = "example"
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 2 ===\n")
                maze.render()
                print("Color changed")

            else:
                print("\033[A\r\033[K", end="")
                print("Invalid command. Try again")
                continue

    except Exception as e:
        print(f"oops something went wrong: {e}")


def version3(maze: Display_Maze, path: str, config: str,
             start_pos: Tuple[int, int] = (0, 0)) -> None:

    width = int(config.get("WIDTH", 10))
    height = int(config.get("HEIGHT", 10))
    exit_point = format_cords(config.get("EXIT", f"{width - 1}, {height - 1}"))

    current_path = path

    try:
        while True:
            prompt = ("Available options:\n"
                      " . m or --maze: generate a new maze\n"
                      " . p or --path: show/unshow shortest path available\n"
                      " . c or --color: change maze color\n"
                      " . q or --quit: exit configuration mode\n"
                      " . clear or --clear: clear maze\n"
                      " command: ")
            command = input(f"\n{prompt}").strip().lower()

            if command == 'q' or command == '--quit':
                break

            elif command == 'm' or command == '--maze':
                maze.build()
                current_path = maze.find_path(start=start_pos, end=exit_point)
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 3 ===\n")
                maze.render()

            elif command == 'p' or command == '--path':
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 3 ===\n")
                if maze.show_path is False:
                    maze.render(path_str=current_path, start_pos=start_pos)
                    maze.show_path = True
                elif maze.show_path is True:
                    maze.render()
                    maze.show_path = False

            elif command == 'c' or command == '--color':
                maze.wall_color = "example"
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 3 ===\n")
                maze.render()
                print("Color changed")

            elif command == 'clear' or command == '--clear':
                print("\033[2J\033[H", end="", flush=True)

            else:
                print("\033[7A\r\033[J", end="")
                print("\nInvalid command. Try again")
                continue

    except Exception as e:
        print(f"oops something went wrong: {e}")


main()
