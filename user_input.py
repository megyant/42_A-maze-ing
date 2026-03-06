from mazeGenerator import MazeGenerator

class maze_alterations:
    def __init__(self, maze: MazeGenerator, path: list[str])




def version1() -> None:
    print("Maze being generated using config.txt")

    print("(Fake maze):\n"
          "┌───┬───────────┐ \n"
          "├─╴ │ ╷ ╶─┬───╴ │ \n"
          "│ ┌─┘ ├─╴ │ ┌───┤ \n"
          "│ └─┐ │ ╶─┤ ╵ ╷ │ \n"
          "├─╴ ├─┴─╴ ├─┬─┘ │ \n"
          "│ ┌─┘ ┌───┘ │ ╶─┤ \n"
          "│ └─╴ │ ╶───┼─╴ │ \n"
          "├─────┘ ╶─┐ ╵ ╶─┤ \n"
          "└─────────┴─────┘ \n")

    maze_color = input("Change wall color? (Y/N): ")

    if maze_color == 'y' or maze_color == 'Y':
        print("wall color changed")
    else:
        print("Oh noo! :(")


def rui_alexandre_version() -> None:
    maz
version1()
