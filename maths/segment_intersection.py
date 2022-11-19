from __future__ import annotations
from math import sqrt


class Point:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def dist(self, other: Point) -> float:
        diff = self - other
        return sqrt((pow(diff.x, 2) + pow(diff.y, 2)))

    def __mul__(self, other: float | int) -> Point:
        if isinstance(other, (float, int)):
            return Point(self.x * other, self.y * other)

        raise TypeError(f'Cannot multiply a point with {type(other)}')

    def __rmul__(self, other) -> Point:
        return self * other

    def __add__(self, other: Point) -> Point:
        if isinstance(other, Point):
            return Point(other.x + self.x, other.y + self.y)

    def __sub__(self, other: Point):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        if isinstance(other, Point):
            return Point(other.x - self.x, other.y - self.y)

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Segment:
    def __init__(self, start: Point, end: Point):
        self.start, self.end = start, end
        self.slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def intersect(self, other: Segment):
        """Returns true if the two segments intersect or overlap"""

        # technique used https://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf
        o1 = self.get_orientation(other.start)
        o2 = self.get_orientation(other.end)
        o3 = other.get_orientation(self.start)
        o4 = other.get_orientation(self.end)

        # General case
        if (o1 != o2) and (o3 != o4):
            return True

        # elif
        special_cases = [
            o1 == 0 and self.on_segment(other.start),  # other.start is on the segment
            o2 == 0 and self.on_segment(other.end),  # other.end is on the segment
            o3 == 0 and self.on_segment(self.start),  # self.start is on other segment
            o4 == 0 and self.on_segment(self.end),  # self.end is on other segment
        ]
        return any(special_cases)

    def get_orientation(self, to: Point) -> float:
        """
        :param to: orientation towards
        :return:  0 -> Collinear points :: 1 -> Clockwise points  :: 2 -> Counterclockwise

        Gets orientation to a third point.
        """
        diff = (self.end.y - self.start.y) * (to.x - self.end.x) - (to.y - self.end.y) * (self.end.x - self.start.x)

        if diff > 0:
            return 1
        elif diff < 0:
            return 2
        return 0

    def on_segment(self, point: Point) -> bool:
        return self.start.dist(point) + self.end.dist(point) == self.start.dist(self.end)  # A----C------B


if __name__ == '__main__':
    p1 = Point(1, 1)
    p2 = Point(3, 3)
    seg1 = Segment(
        Point(1, 1), Point(3, 3)
    )
    seg2 = Segment(
        Point(2, 1), Point(4, 3)
    )
    print(seg1.intersect(seg2))
