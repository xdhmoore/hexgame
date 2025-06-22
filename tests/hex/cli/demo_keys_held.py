

from blessed import Terminal


def point_generator(width, height):
    while True:
        for y in range(height):
            for x in range(width):
                yield (x, y)

# RESUME - make key state class that changes key state based on key events instead of acting
# on key presses


def main() -> None:
    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.home + term.clear)
        point_gen = point_generator(term.width, term.height)
        while True:
            if (term.kbhit(0)):
                key = term.getch()
                point = next(point_gen)
                print(term.move_xy(*point) + "0", end="", flush=True)


if __name__ == "__main__":
    main()
