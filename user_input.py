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
    print("\n=== Version 1 ===\n")
    maze.render()
    # path_str=path_str, start_pos=entry
    version1()

    print("\033[2J\033[H", end="", flush=True)

    print("\n=== Version 2 ===\n")

    maze.build()
    maze.render()
    rui_alexandre_version(maze, path_str, config)


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

            if command.lower() == 'q':
                break

            elif command.lower() == 'r':
                maze.build()
                current_path = maze.find_path(start=start_pos, end=exit_point)
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 2 ===\n")
                maze.render()

            elif command.lower() == 'p':
                print("\033[2J\033[H", end="", flush=True)
                print("\n=== Version 2 ===\n")
                maze.render(path_str=current_path, start_pos=start_pos)

            elif command.lower() == 'c':
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


def version1() -> None:

    maze_color = input("\nChange wall color? (Y/N): ")

    if maze_color == 'y' or maze_color == 'Y':
        print("wall color changed")
    else:
        print("Oh noo! :(")


main()
