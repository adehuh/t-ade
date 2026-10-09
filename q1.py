def draw_circle(radius: int = 19, thickness: int = 3) -> str:
    if radius < 1 or not 1 <= thickness <= radius:
        raise ValueError("Require radius >= 1 and 1 <= thickness <= radius")

    inner_squared = (radius - thickness) ** 2
    outer_squared = radius * radius
    squares = [x * x for x in range(-radius - 1, radius + 2)]
    rows = []

    for y_squared in squares:
        rows.append("".join(
            "." if inner_squared < x_squared + y_squared < outer_squared else "#"
            for x_squared in squares
        ))

    return "\n".join(rows)


if __name__ == "__main__":
    radius = 19
    thickness = 3

    print(draw_circle(radius, thickness))
