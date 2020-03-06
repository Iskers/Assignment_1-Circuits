import copy
import sys
from .parts import *


class Circuit:
    """
    :ivar _canvas: List of parts in circuit.
    :ivar _name: Circuits name.
    :ivar _inside_diameter: Inside diameter of pipes, must be the same for all pipes.
    :ivar _efficiency: Efficiency of the pump in the circuit.
    """

    def __init__(self):
        # Circuit basics
        self._name = ""
        self._validness = True

        # Circuit specifics
        self._canvas: list = []
        self._inside_diameter: float = 0.0
        self._height = None
        self._efficiency = 0
        self._filter_count = 0
        self._valve_count = 0

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.canvas[item]
        elif isinstance(item, Part):
            return self.canvas.index(item)
        else:
            raise Exception("Cant get item")

    def __str__(self):
        return "Circuit " + self.name

    def __enter__(self):
        """Enter exit used in context where you want to alter a circuit, but revert back when finished. Used in
        study_.py"""
        self._name_backup = self.name
        self._validness_backup = self._validness
        self._canvas_backup = copy.deepcopy(self.canvas)
        self._inside_diameter_backup = self.inside_diameter
        self._height_backup = self.height
        self._efficiency_backup = self.efficiency
        self._filter_count_backup = self.filter_count
        self._valve_count_backup = self.valve_count
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.name = self._name_backup
        self._validness = self._validness_backup
        self.canvas = self._canvas_backup
        self.inside_diameter = self._inside_diameter_backup
        self._height = self._height_backup
        self.efficiency = self._efficiency_backup
        self.filter_count = self._filter_count_backup
        self.valve_count = self._valve_count_backup
        del self._name_backup, self._validness_backup, self._canvas_backup, self._inside_diameter_backup, \
            self._height_backup, self._efficiency_backup, self._filter_count_backup, self._valve_count_backup

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, value: list):
        self._canvas = value

    def canvas_insert(self, index, part: Part):
        self.canvas.insert(index, part)

    @property
    def height(self):
        if self._height is None:
            height = 0
            for part in self.canvas:
                if isinstance(part, PipeStraight):
                    if part.angle > 0:
                        height += part.length
            self._height = height
        return self._height

    @height.setter
    def height(self, value):
        if value is None:
            self._height = None
        else:
            raise Exception(f"You are not allowed to directly change the circuit height.")

    @property
    def filter_count(self):
        return self._filter_count

    @filter_count.setter
    def filter_count(self, value):
        self._filter_count = value

    @property
    def valve_count(self):
        return self._valve_count

    @valve_count.setter
    def valve_count(self, value):
        self._valve_count = value

    @property
    def inside_diameter(self):
        if self._inside_diameter == 0:
            for part in self.canvas:
                if isinstance(part, Pipe):
                    self._inside_diameter = part.inside_diameter
                    break
        return self._inside_diameter

    @inside_diameter.setter
    def inside_diameter(self, value):
        for part in self.canvas:
            if isinstance(part, Pipe):
                part.inside_diameter = value
        self._inside_diameter = value

    @property
    def efficiency(self):
        if self._efficiency == 0:
            for part in self.canvas:
                if isinstance(part, Pump):
                    if part.efficiency <= 0 or part.efficiency > 1:
                        raise Exception("Efficiency must be from 0 to 1")
                    else:
                        self._efficiency = part.efficiency
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        for part in self.canvas:
            if isinstance(part, Pump):
                if value <= 0 or value > 1:
                    raise Exception("Efficiency must be from 0 to 1")
                else:
                    part.efficiency = value
                    self._efficiency = part.efficiency

    def add_part(self, part: Part):
        self.canvas.append(part)
        return self.canvas

    def add_part_from_string(self, line):
        part_creator = Part()
        self.canvas.append(part_creator.part_from_string(line))
        return self.canvas

    # Main Adding methods
    def add_tank(self, name: str):
        tank = Tank(name)
        self.canvas.append(tank)
        return tank

    def add_straight_pipe(self, name: str, inside_diameter: float, length: float, angle: int):
        pipe = PipeStraight(name, inside_diameter, length, angle)
        self.canvas.append(pipe)
        return pipe

    def add_bend_pipe(self, name: str, inside_diameter: float):
        pipe = PipeBend(name, inside_diameter)
        self.canvas.append(pipe)
        return pipe

    # Set default for easy part creation
    def add_pump(self, name: str, efficiency: float = 0.9):
        pump = Pump(name, efficiency)
        self.canvas.append(pump)
        return pump

    def add_filter(self, name: str, cleanliness: bool):
        filter_created = Filter(name, cleanliness)
        self.canvas.append(filter_created)
        self.filter_count += 1
        return filter

    def add_valve(self, name: str, openness: bool):
        valve = Valve(name, openness)
        self.canvas.append(valve)
        self.valve_count += 1
        return valve

    # TODO Remove
    # Legacy Not in use
    def add_part_nested(self, line):  # pragma: no cover
        current_angle = 0
        horizontalness = True

        try:
            part_type = line[0]
        except IndexError as ix:
            sys.stderr.write("Missing value : {}".format(ix) + '\n')
        else:
            part_type = part_type.lower()

            if part_type == "tank":
                try:
                    self.add_tank(line[1])
                except IndexError as ix:
                    sys.stderr.write("Missing value : {}".format(ix) + '\n')

            elif part_type == "pipe":
                try:
                    self.add_straight_pipe(line[1], float(line[3]), int(float(line[2])), horizontalness)
                except IndexError as ix:
                    sys.stderr.write("Missing value : {}".format(ix) + '\n')
                except ValueError as ve:
                    sys.stderr.write("Wrong format : {}".format(ve) + '\n')

            elif part_type == "bend":
                try:
                    self.add_bend_pipe(line[1], float(line[2]))
                except IndexError as ix:
                    sys.stderr.write("Missing value : {}".format(ix) + '\n')
                except ValueError as ve:
                    sys.stderr.write("Wrong format : {}".format(ve) + '\n')
                else:
                    horizontalness = not horizontalness

            elif part_type == "pump":
                try:
                    self.add_pump(line[1], float(line[2]))
                except IndexError as ix:
                    sys.stderr.write("Missing value : {}".format(ix) + '\n')
                except ValueError as ve:
                    sys.stderr.write("Wrong format : {}".format(ve) + '\n')

            elif part_type == "valve":
                try:
                    self.add_valve(line[1], bool(line[2]))
                except IndexError as ix:
                    sys.stderr.write("Missing value : {}".format(ix) + '\n')
                except ValueError as ve:
                    sys.stderr.write("Wrong format : {}".format(ve) + '\n')

            elif part_type == "filter":
                try:
                    self.add_filter(line[1], bool(line[2]))
                except IndexError as ix:
                    sys.stderr.write("Missing value : {}".format(ix) + '\n')
                except ValueError as ve:
                    sys.stderr.write("Wrong format : {}".format(ve) + '\n')

            else:
                sys.stderr.write("{} not a valid part".format(part_type) + '\n')


class CanvasCreator(Circuit):  # pragma: no cover
    def __init__(self):
        super().__init__()
        self.tank_count = 0
        self.pump_count = False
        self.tank_count = 0
        self.current_angle = 0

    def canvas_creator(self):

        print("First we create a supplying tank. \n")
        tank_name = input("Please give this tank a name: ")
        self.canvas.append(Tank(tank_name))
        self.tank_count += 1

        while not self.inside_diameter:
            try:
                self.inside_diameter = float(input("\nPlease set the inside diameter for the circuit: "))
            except ValueError:
                print("Invalid inside diameter, expected integer")
        print("\nThe second element must be a horizontal pipe. \n")
        self.pipe_creator()

        while self.tank_count < 2 and self.validness is True:
            print('\n' + "Current circuit: ")
            print(self.canvas)
            print('\n')
            self.part_creator()

    def part_creator(self):
        user_input = input("Please pick a part to add to the circuit: ")
        user_input = user_input.lower()

        if user_input == "tank":
            self.canvas.append(Tank(input("Input the final tank name: ")))
            self.tank_count += 1

        elif user_input == "pipe":
            self.pipe_creator(self.current_angle)
            # try:
            #     self.pipe_creator(bool(input("Is the pipe horizontal? [1/0] ")))
            # except TypeError as tp:
            #     print("Expected bool, {}".format(tp))

        elif user_input == "bend":
            if isinstance(self.canvas[-1], Pipe):
                self.bend_creator()
                # Change for varying angles
                if self.current_angle == 0:
                    self.current_angle = 90
                else:
                    self.current_angle = 0
            else:
                print("Not allowed to create bend.")

        elif user_input == "pump":
            if self.horizontal_pipe_test():
                self.pump_creator()
                self.pipe_creator()
            else:
                print("Error creating pump, previous part is not a horizontal pipe.")
            pass

        elif user_input == "filter":
            if self.horizontal_pipe_test():
                self.filter_creator()
                self.pipe_creator()
            else:
                print("Error creating filter, previous part is not a horizontal pipe.")
            pass

        elif user_input == "valve":
            if isinstance(self.canvas[-1], Pipe):
                self.valve_creator()
                self.pipe_creator(self.canvas[-2].get_angle())
            else:
                print("Error creating valve, previous part is not a pipe ")

        else:
            print("Invalid input, expected Part type")

    def pipe_creator(self, angle: int = 0):
        pipe_name = input("Please give this pipe a name: ")
        length = 0
        while not length:
            try:
                length = int(input("Please set the length of the pipe {}: ".format(pipe_name)))
            except ValueError:
                print("Invalid length, expected integer")
            else:
                self.canvas.append(PipeStraight(pipe_name, self.inside_diameter, length, angle))

    def bend_creator(self, horizontalness: bool = True):
        pipe_name = input("Please give this bend pipe a name: ")
        self.canvas.append(PipeBend(pipe_name, self.inside_diameter))  # , horizontalness

    def horizontal_pipe_test(self):
        if isinstance(self.canvas[-1], PipeStraight):
            if self.canvas[-1].get_angle() == 0:
                return True
        return False

    def pump_creator(self):
        pump_name = input("Please give this pump a name: ")
        try:
            efficiency = float(input("Please input efficiency: "))
        except TypeError:
            print("Expected float number")
        else:
            self.canvas.append(Pump(pump_name, efficiency))
            self.pump_count = True

    def valve_creator(self):
        valve_name = input("Please give this valve a name: ")
        try:
            openness = bool(input("Is this valve open or half-open? [1/0]"))
        except TypeError:
            print("Expected float number")
        else:
            self.canvas.append(Valve(valve_name, openness))

    def filter_creator(self):
        filter_name = input("Please give this filter a name: ")
        try:
            cleanliness = bool(input("Is this filter clean? [1/0]"))
        except TypeError:
            print("Expected float number")
        else:
            self.canvas.append(Filter(filter_name, cleanliness))
