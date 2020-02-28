from .parts2 import *


class Circuit:
    tank_count: int
    pump_count: bool
    inside_diameter: int = False
    validness: bool
    canvas: list = []

    def __init__(self):
        self.validness = True
        self.tank_count = 0
        self.pump_count = 0
        self.inside_diameter: int = False
        self.canvas: list = []

    def canvas_creator(self):
        current_part = 0
        part_creator = PartCreator(self)

        print("First we create a supplying tank. \n")
        tank_name = input("Please give this tank a name: ")
        self.canvas.append(Tank(tank_name))
        self.tank_count += 1

        while not self.inside_diameter:
            try:
                self.inside_diameter = int(input("\nPlease set the inside diameter for the circuit: "))
            except ValueError:
                print("Invalid inside diameter, expected integer")
        print("\nThe second element must be a horizontal pipe. \n")
        part_creator.pipe_creator(1)

        while self.tank_count < 2 and self.validness is True:
            print('\n' + "Current circuit: ")
            print(self.canvas)
            print('\n')
            part_creator.add_part(Circuit)


class PartCreator:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit

    def add_part(self, circuit: Circuit):
        user_input = input("Please pick a part to add to the circuit: ")
        user_input = user_input.lower()

        if user_input == "tank":
            circuit.canvas.append(Tank(input("Input the final tank name: ")))
            circuit.tank_count += 1

        elif user_input == "pipe":
            if isinstance(self.circuit.canvas[-1], Pipe):
                reference_pipe = self.circuit.canvas[-1]
                self.pipe_creator(reference_pipe.get_horizontalness)
            else:
                try:
                    self.pipe_creator(bool(input("Is the pipe horizontal? [1/0] ")))
                except TypeError as tp:
                    print("Expected bool, {}".format(tp))

        elif user_input == "bend":
            if isinstance(self.circuit.canvas[-1], Pipe):
                reference_pipe = self.circuit.canvas[-1]
                self.bend_creator(reference_pipe.get_horizontalness)
            else:
                self.pipe_creator(not bool(input("Does the bend end vertical? [1/0] ")))

        elif user_input == "pump":
            pass

        else:
            pass

    def pipe_creator(self, horizontalness: bool = True):
        pipe_name = input("Please give this pipe a name: ")
        length = 0
        while not length:
            try:
                length = int(input("Please set the length of the pipe {}: ".format(pipe_name)))
            except ValueError:
                print("Invalid length, expected integer")
            else:
                self.circuit.canvas.append(
                    PipeStraight(pipe_name, self.circuit.inside_diameter, length, horizontalness))

    def bend_creator(self, horizontalness: bool = True):
        pipe_name = input("Please give this bend pipe a name: ")
        horizontalness = not horizontalness
        self.circuit.canvas.append(PipeBend(pipe_name, self.circuit.inside_diameter, horizontalness))

    def horizontal_pipe_test(self, pre_part: Part):
        if isinstance(pre_part, PipeStraight):
            if pre_part.horizontalness:
                return True
        return False

    def pump_creator(self):

        pass

    def valve_creator(self):
        pass

    def filter_creator(self):
        pass
