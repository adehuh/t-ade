class Ring:
    def __init__(self, cx: int, cy: int, radius: int, thickness: int) -> None:
        if radius < 1 or not 1 <= thickness <= radius:
            raise ValueError("Require radius >= 1 and 1 <= thickness <= radius")

        self.cx = cx
        self.cy = cy
        self._inner_squared = (radius - thickness) ** 2
        self._outer_squared = radius * radius

    def contains(self, x: int, y: int) -> bool:
        dx = x - self.cx
        dy = y - self.cy
        return self._inner_squared < dx * dx + dy * dy < self._outer_squared


class Canvas:
    def __init__(self, size: int, background: str = "#") -> None:
        if size < 1:
            raise ValueError("Size must be positive")
        if len(background) != 1:
            raise ValueError("Background must be one character")

        self._cells = [[background] * size for _ in range(size)]

    def draw(self, shape, char: str = ".") -> None:
        if len(char) != 1:
            raise ValueError("Drawing character must be one character")

        contains = shape.contains
        for y, row in enumerate(self._cells):
            for x in range(len(row)):
                if contains(x, y):
                    row[x] = char

    def render(self) -> str:
        return "\n".join("".join(row) for row in self._cells)


def main() -> None:
    size = 41
    radius = 19
    thickness = 3
    background = "#"
    char = "."
    centre = size // 2

    ring = Ring(cx=centre, cy=centre, radius=radius, thickness=thickness)
    canvas = Canvas(size=size, background=background)
    canvas.draw(ring, char=char)
    print(canvas.render())


if __name__ == "__main__":
    main()
