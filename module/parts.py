import math
from pytypes import typechecked


# noinspection PyAttributeOutsideInit
@typechecked
class Part:
    """
    Part is a abstract class for the parts in a circuit.

    Part list: Tank, PipeStraight, PipeBend, Pump, Valve, Filter
    """

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @classmethod
    def factory_function(cls, **kwargs):
        parts_dict = {"tank": "Tank", "pipe": "PipeStraight", "bend": "PipeBend", "pump": "Pump",
                      "filter": "Filter", "valve": "Valve"}
        return globals()[parts_dict[kwargs["type_"]]].initialize_with_kwargs(**kwargs)

    @classmethod
    def part_from_string(cls, *args):
        """
        Main method for creating classes from strings in a file. Redirects too each class initialize from string
        function.

        :param args: Required class arguments
        :return: Object of class_name type
        :rtype: object
        """
        parts_dict = {"tank": "Tank", "pipe": "PipeStraight", "bend": "PipeBend", "pump": "Pump",
                      "filter": "Filter", "valve": "Valve"}
        object_name = parts_dict[args[0][0]]
        object_created = globals()[object_name].initialize_with_args(*args)
        return object_created

    def calculate_losses_of_pressure(self, density_of_medium: int, velocity_of_medium, flow_coefficient: float):
        """Default calculation of losses of pressure, to be overwritten by functions with special cases.

        :param density_of_medium: Density of the medium where pressure is calculated.
        :param velocity_of_medium: Velocity of the medium where pressure is calculated.
        :param flow_coefficient: Flow coefficient of the medium where pressure is calculated.
        :return: Loss of pressure
        :rtype float:
        """

        return self.ZETA * density_of_medium / 2 * velocity_of_medium ** 2


@typechecked
class Tank(Part):
    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return "Tank " + self.name

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'{self.name})'

    @classmethod
    def initialize_with_args(cls, *args):
        tank = cls(args[0][1])
        return tank

    @classmethod
    def initialize_with_kwargs(cls, **kwargs):
        tank = cls(name=kwargs["name"])
        return tank

    def calculate_losses_of_pressure(*args):
        return 0


class Pipe(Part):
    """
    Abstract class for pipes. Should not be initialized.

    :param str name: Name of part
    :param float inside_diameter: Inside diameter of pipe
    """

    def __init__(self, name: str, inside_diameter: float):
        self._name = name
        self._inside_diameter = inside_diameter

    @property
    def inside_diameter(self):
        return self._inside_diameter

    @inside_diameter.setter
    def inside_diameter(self, value):
        self._inside_diameter = value


class PipeStraight(Pipe):
    def __init__(self, name: str, inside_diameter: float, length: float, angle: int = 0):
        super().__init__(name, inside_diameter)
        self._length = length
        self._angle = angle

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, inside_diameter={self.inside_diameter}," \
               f" length={self.length}, angle={self.angle})"

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value < 0 | value > 360:
            raise Exception(f"Invalid angle, should be between 0 and 360, tried to set to {value}")
        self._angle = value

    @property
    def length(self):
        return self._length

    @typechecked
    @length.setter
    def length(self, value: float):
        if value < 1:
            raise Exception(f"Length has to be 1 or more, tried to set to {value}")
        self._length = value

    def calculate_losses_of_pressure(self, density_of_medium: int, velocity_of_medium, flow_coefficient: int):
        return flow_coefficient * (1 / self.inside_diameter) * (density_of_medium / 2) * velocity_of_medium

    @classmethod
    def initialize_with_args(cls, *args):
        pipe = cls(args[0][1], float(args[0][3]), float(args[0][2]), int(float(args[0][4])))
        return pipe

    @classmethod
    def initialize_with_kwargs(cls, **kwargs):
        return cls(name=kwargs["name"], inside_diameter=float(kwargs["diameter"]),
                   length=float(kwargs["length"]), angle=int(float(kwargs["angle"])))


class PipeBend(Pipe):
    def __init__(self, name: str, inside_diameter: float):
        super().__init__(name, inside_diameter)
        self.ZETA = 0.1 * math.sin(math.pi / 2)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @classmethod
    def initialize_with_args(cls, *args):
        pipe = cls(args[0][1], float(args[0][2]))
        return pipe

    @classmethod
    def initialize_with_kwargs(cls, **kwargs):
        return cls(name=kwargs["name"], inside_diameter=float(kwargs["diameter"]))


class Pump(Part):
    def __init__(self, name: str, efficiency: float):
        self._name = name
        self._efficiency = efficiency

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, efficiency={self.efficiency})"

    @property
    def efficiency(self):
        return self._efficiency

    @typechecked
    @efficiency.setter
    def efficiency(self, value: float):
        self._efficiency = value

    @classmethod
    def initialize_with_args(cls, *args):
        pipe = cls(args[0][1], float(args[0][2]))
        return pipe

    @classmethod
    def initialize_with_kwargs(cls, **kwargs):
        return cls(name=kwargs["name"], efficiency=float(kwargs["efficiency"]))

    def calculate_losses_of_pressure(self, *args):
        return 0


class Filter(Part):
    def __init__(self, name: str, cleanliness: bool, **extra_kwarg):
        self._name = name
        self._cleanliness = cleanliness
        self.ZETA = self._get_ZETA_from_cleanliness(cleanliness)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, cleanliness={self.cleanliness})"

    @property
    def cleanliness(self):
        return self._cleanliness

    @typechecked
    @cleanliness.setter
    def cleanliness(self, value: bool):
        self._cleanliness = value
        self.ZETA = self._get_ZETA_from_cleanliness(value)

    @classmethod
    def initialize_with_args(cls, *args):
        pipe = cls(args[0][1], bool(args[0][2]))
        return pipe

    @classmethod
    def initialize_with_kwargs(cls, **kwargs):
        return cls(**kwargs)

    @staticmethod
    def _get_ZETA_from_cleanliness(openness: bool) -> float:
        if openness:
            ZETA = 0.5
        else:
            ZETA = float(5)
        return ZETA


class Valve(Part):
    def __init__(self, name: str, openness: bool):
        self._name = name
        self._openness = openness
        self.ZETA = self.get_ZETA_from_openness(openness)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, openness={self.openness})"

    @property
    def openness(self):
        return self._openness

    @typechecked
    @openness.setter
    def openness(self, value: bool):
        self._openness = value
        self.ZETA = self.get_ZETA_from_openness(value)

    @classmethod
    def initialize_with_args(cls, *args):
        pipe = cls(args[0][1], bool(args[0][2]))
        return pipe

    @classmethod
    def initialize_with_kwargs(cls, **kwargs):
        return cls(name=kwargs["name"], openness=bool(kwargs["opening"]))

    @staticmethod
    def get_ZETA_from_openness(openness: bool) -> float:
        if openness:
            ZETA = 0.2
        else:
            ZETA = float(4)
        return ZETA
