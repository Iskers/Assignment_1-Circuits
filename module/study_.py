from pytypes import typechecked
import matplotlib.pyplot as plt
import numpy as np

import module.circuit as cir
import module.circuit_calculator as calc
import module.path_finder as pf


class Study:
    def __init__(self):
        self._velocity_of_medium = 5

    @property
    def velocity_of_medium(self):
        return self._velocity_of_medium

    @velocity_of_medium.setter
    def velocity_of_medium(self, value):
        self._velocity_of_medium = value

    def png_generator_plot(self, circuit: cir.Circuit):
        for i in range(1, 6):
            self.velocity_of_medium = i

            plt.figure(0)
            self.plot_changing_type(circuit, "inside_diameter", "Inside diameter study")
            plt.figure(1)
            self.plot_changing_type(circuit, "efficiency", "Efficiency study", steps=90)
            plt.figure(2)
            self.plot_changing_type(circuit, "height", "Height study", start=2, stop=10, steps=9)

    def base_study(self, circuit: cir.Circuit):
        for i in range(1, 5):
            self.velocity_of_medium = i
            print(f"Study with velocity = {self.velocity_of_medium}")
            print(f"Circuit with varying efficiency: \n{self._stepper_range(circuit, 'efficiency', 1, 0.1, 10)[0]}\n")
            print(f"Circuit with varying inside_diameter: "
                  f"\n{self._stepper_range(circuit, 'inside_diameter', 0.1, 1, 10)[0]}\n")
            print(f"Circuit with varying height: \n{self._stepper_range(circuit, 'height', 2, 10, 9)[0]}\n")
            print(f"Circuit with varying Valve settings: \n{self._stepper_bool(circuit, 'Valve')[0]}\n")
            print(f"Circuit with varying Filter settings: \n{self._stepper_bool(circuit, 'Filter')[0]}\n")

    def _stepper_range(self, circuit, type_, start: float, stop: float, steps: int):
        energy_consumptions = []
        list_ = np.linspace(start, stop, steps)
        with circuit as test_circuit:
            if type_ == "height":
                for i in range(len(list_)):
                    self._canvas_height_adapt(test_circuit, list_[i])
                    self._append_energy_consumption(test_circuit, energy_consumptions)
            else:
                for i in range(len(list_)):
                    setattr(test_circuit, type_, list_[i])
                    self._append_energy_consumption(test_circuit, energy_consumptions)
        return energy_consumptions, list_

    def _stepper_bool(self, circuit: cir.Circuit, type_) -> list:
        if type_ == "Valve":
            attribute = "openness"
            return self._stepper_type(circuit, type_, attribute)
        elif type_ == "Filter":
            attribute = "cleanliness"
            return self._stepper_type(circuit, type_, attribute)
        else:
            raise Exception(f"Invalid type, expected Valve, or Filter, given {type_}")

    # Uses eval, should only be run when tested type_
    def _stepper_type(self, circuit: cir.Circuit, type_, attribute: str) -> list:
        """
        Takes in a circuit and changes the valves or filters to give different results.

        :param circuit: Circuit to analyze
        :param type_: String with value "Valve" or "Filter"
        :param attribute: Attribute connected to type_ class.
        :return: List of energy consumption.
        """
        energy_consumptions = []

        with circuit as test_circuit:
            for part in test_circuit.canvas:
                if isinstance(part, eval("cir." + type_)):
                    setattr(part, attribute, True)

            self._append_energy_consumption(test_circuit, energy_consumptions)
            for part in test_circuit.canvas:
                if isinstance(part, eval("cir." + type_)):
                    setattr(part, attribute, False)
                    self._append_energy_consumption(test_circuit, energy_consumptions)
        return energy_consumptions

    def _canvas_height_adapt(self, circuit, height: float) -> int:
        """
        Inserts a vertical straight pipe with the given length to the given circuit

        :param circuit: Some Circuit
        :param height:
        :return: height
        """
        if height == 0.0 and circuit.height > 0.0:
            raise Exception(f"Removing height from a circuit with height not allowed as this"
                            f" fundamentally changes the circuit. This requires removing all bends and content between."
                            f" Height of circuit is {circuit.height}")

        delta = circuit.height - height
        delta = abs(delta)
        if circuit.height > height:
            for part in circuit.canvas:
                if isinstance(part, cir.PipeStraight):
                    if part.angle > 0:
                        if part.length < delta:
                            length_allowed_to_remove = part.length - 1
                            part.length -= length_allowed_to_remove
                            delta -= length_allowed_to_remove
                        else:
                            part.length -= delta
                            circuit.height = None
                            return circuit.height
            raise Exception(f"Not allowed to remove {height} from {circuit}")

        elif circuit.height < height:
            pipe = cir.PipeStraight("Added_pipe", circuit.inside_diameter, delta, 90)
            self._add_parts_to_canvas(circuit, pipe)
            circuit.height = None
            return circuit.height

    @typechecked
    def _add_parts_to_canvas(self, circuit: cir.Circuit, part_to_be_added: cir.Part, amount: int = 1) -> None:
        """
        Adds a given part to a circuit at a given position. Only to be used in Study Class as it adds with
        certain assumptions.

        :param circuit: Given circuit
        :param part_to_be_added: Part to be added
        :param amount: # of part to be added to add
        :return: None
        """
        if isinstance(part_to_be_added, cir.PipeStraight):
            if part_to_be_added.angle > 0:
                for part_in_canvas in circuit.canvas:
                    if isinstance(part_in_canvas, cir.PipeStraight):
                        if part_in_canvas.angle > 0:
                            for i in range(amount):
                                index = circuit[part_in_canvas]
                                circuit.canvas_insert(index + 1, part_to_be_added)
                            break

    def _append_energy_consumption(self, circuit: cir.Circuit, list_: list):
        calculator = calc.CircuitCalculator(velocity_of_medium=self.velocity_of_medium)
        data = calculator.calculate_actual_energy_for_circuit(circuit)
        data = round(data, 2)
        list_.append(data)

    def plot_changing_type(self, circuit, type_, file_name, start=0.1, stop=1, steps=10):
        if type_ == "inside_diameter":
            y_values, x_values = self._stepper_range(circuit, type_, start, stop, steps)
            self._plot_image_generator(x_values, y_values, f"Increasing inside diameter", "Energy consumption",
                                       f"Study inside diameter", file_name,
                                       label=f"Velocity = {str(self.velocity_of_medium)}")

        elif type_ == "efficiency":
            y_values, x_values = self._stepper_range(circuit, type_, start, stop, steps)
            self._plot_image_generator(x_values, y_values, f"Decreasing efficiency", "Energy consumption",
                                       f"Study efficiency", file_name,
                                       label=f"Velocity = {str(self.velocity_of_medium)}")

        elif type_ == "height":
            y_values, x_values = self._stepper_range(circuit, type_, start, stop, steps)
            self._plot_image_generator(x_values, y_values, f"Increasing height", "Energy consumption",
                                       f"Study height", file_name,
                                       label=f"Velocity = {str(self.velocity_of_medium)}")

    @staticmethod
    def _plot_image_generator(x_values, y_values, x_label, y_label, title, file_name, label=""):
        plt.plot(x_values, y_values, label=label)
        plt.title(title)
        plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        path = pf.PathFinder.get_pure_path("templates")
        file_path = f"/{path}/{file_name}"
        plt.savefig(file_path)
        return file_name
