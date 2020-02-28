import math
from pytypes import typechecked


@typechecked
class Part:
    """
    Part list:
    \n Tanks:
    Tanks have just a name.
    \n Pipes:
    Pipes have a name, an inside diameter, a length and an
    angle. To simplify, we shall assume that circuits are made only of horizontal and vertical pipes, i.e. that the
    angle of a pipe is either 0 or 90 degrees. To simplify, we shall assume that inside diameters and lengths of
    pipes are measured in meters.
    \n Bends:
    Bends make it possible to pass from horizontal to vertical pipes and
    vice-versa. They have a name and an inside diameter. As we consider only horizontal and vertical pipes,
    all bends have a 90 degrees angle. To simplify, we shall assume that inside diameters of bends are measured in
    meters.
    \n Pumps:
    Pumps have a name and an efficiency. The latter varies between 0.7 and 0.9 depending on the pump
    and motor configuration.
    \n Valves:
    Valves have a name and can be more or less open, which has indeed an influence
    on frictions and therefore pressure losses. To simplify, we shall assume that valves are either fully or half
    open.
    \n Filters:
    Filters have a name and can be more or less dirty, which has indeed an influence on frictions
    and therefore pressure losses. To simplify, we shall assume that filters are either new (clean) or used (dirty).\n
    """

    parts_dict = {"tank": "Tank", "pipe": "PipeStraight", "bend": "PipeBend", "pump": "Pump",
                  "filter": "Filter", "valve": "Valve"}

    @classmethod
    def part_from_string(cls, class_name, *args, **kwargs):
        class_name = cls.parts_dict[class_name]
        class_created = globals()[class_name].initialize_from_string(*args)
        return class_created

    def calculate_losses_of_pressure(self, density_of_medium: int, velocity_of_medium: int, flow_coefficient: float):
        return self.ZETA * density_of_medium / 2 * velocity_of_medium ** 2


@typechecked
class Tank(Part):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'{self.name})'

    @classmethod
    def initialize_from_string(cls, *args):
        tank = cls(args[0][1])
        return tank

    def calculate_losses_of_pressure(*args):
        return 0


class Pipe(Part):
    angle: int
    horizontalness: bool

    def __init__(self, name: str, inside_diameter: float):
        self.name = name
        self.inside_diameter = inside_diameter

    def get_horizontalness(self):
        return self.horizontalness

    def get_inside_diameter(self):
        return self.inside_diameter

    @classmethod
    def initialize_from_string(cls, *args):
        pipe = cls(args[0][1], args[0][2])
        return pipe


class PipeStraight(Pipe):
    def __init__(self, name: str, inside_diameter: float, length: int, horizontalness: bool = True):
        super().__init__(name, inside_diameter)
        self.length = length
        self.horizontalness = horizontalness
        if horizontalness:
            self.angle = 0
        else:
            self.angle = 90

    def __repr__(self):
        if self.horizontalness:
            horizontal_string = "horizontal"
        else:
            horizontal_string = "vertical"
        return f"{self.__class__.__name__} ({self.name}, {self.inside_diameter}, {self.length} {horizontal_string})"

    def calculate_losses_of_pressure(self, density_of_medium: int, velocity_of_medium: int, flow_coefficient: int):
        return flow_coefficient * (1 / self.inside_diameter) * (density_of_medium / 2) * velocity_of_medium

    @classmethod
    def initialize_from_string(cls, *args):
        if float(args[0][4]) == 90:
            horizontalness = False
        else:
            horizontalness = True
        pipe = cls(args[0][1], float(args[0][3]), int(float(args[0][2])), horizontalness)
        return pipe


class PipeBend(Pipe):
    def __init__(self, name: str, inside_diameter: float, horizontalness: bool = False):
        super().__init__(name, inside_diameter)
        self.horizontalness = horizontalness
        self.ZETA = 0.1 * math.sin(math.pi / 2)

    def __repr__(self):
        if self.horizontalness:
            horizontal_string = "horizontal"
        else:
            horizontal_string = "vertical"
        return f"{self.__class__.__name__} ({self.name}, {horizontal_string})"

    @classmethod
    def initialize_from_string(cls, *args):
        pipe = cls(args[0][1], float(args[0][2]))
        return pipe


class Pump(Part):
    def __init__(self, name: str, efficiency: float):
        self.name = name
        self.efficiency = efficiency

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.name}, {self.efficiency})"

    @classmethod
    def initialize_from_string(cls, *args):
        pipe = cls(args[0][1], float(args[0][2]))
        return pipe

    def get_efficiency(self):
        return self.efficiency

    def calculate_losses_of_pressure(self, *args):
        return 0


class Filter(Part):
    def __init__(self, name: str, cleanliness: bool):
        self.name = name
        self.cleanliness = cleanliness
        if cleanliness:
            self.ZETA = 0.5
        else:
            self.ZETA = float(5)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.name}, {self.cleanliness})"

    @classmethod
    def initialize_from_string(cls, *args):
        pipe = cls(args[0][1], bool(args[0][2]))
        return pipe


class Valve(Part):
    def __init__(self, name: str, openness: bool):
        self.name = name
        self.openness = openness
        if openness:
            self.ZETA = 0.2
        else:
            self.ZETA = float(4)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.name}, {self.openness})"

    @classmethod
    def initialize_from_string(cls, *args):
        pipe = cls(args[0][1], bool(args[0][2]))
        return pipe
