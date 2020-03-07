from pytypes import typechecked
import matplotlib.pyplot as plt
import numpy as np

import module.circuit as cir
import module.circuit_calculator as calc
import module.path_finder as pf


class Study:
    def __init__(self, velocity=5):
        self._velocity_of_medium = velocity

    @property
    def velocity_of_medium(self):
        return self._velocity_of_medium

    @velocity_of_medium.setter
    def velocity_of_medium(self, value):
        self._velocity_of_medium = value

    def png_generator_plot(self, circuit: cir.Circuit, velocity_range, diameter_range, efficiency_range, height_range):
        file_names = ("Inside diameter study.png", "Efficiency study.png", "Height study.png")
        for i in range(velocity_range[0], velocity_range[1] + 1, velocity_range[2]):
            self.velocity_of_medium = i
            plt.figure(0)
            self.plot_changing_type(circuit, "inside_diameter", file_names[0], start=diameter_range[0],
                                    stop=diameter_range[1], steps=diameter_range[2])
            plt.figure(1)
            self.plot_changing_type(circuit, "efficiency", file_names[1], start=efficiency_range[0],
                                    stop=efficiency_range[1], steps=efficiency_range[2])
            plt.figure(2)
            self.plot_changing_type(circuit, "height", file_names[2], start=height_range[0], stop=height_range[1],
                                    steps=height_range[2])
        for i in range(3):
            plt.figure(i)
            plt.clf()
        return file_names

    def boolean_study(self, circuit):
        valve_study = []
        filter_study = []
        velocities = []
        for i in range(1, 5 + 1):
            self.velocity_of_medium = i

            valve_study.append(self._stepper_boolean(circuit, "Valve"))
            filter_study.append(self._stepper_boolean(circuit, "Filter"))
            velocities.append(i)
        return valve_study, filter_study, velocities

    def circuit_performance(self, circuit):
        calculator = calc.CircuitCalculator(self.velocity_of_medium)
        reynolds_number = calculator.calculate_reynolds_number(circuit)
        heights_losses, frictions_losses, flow = calculator.calculate_core_attributes(circuit)
        theoretical_energy = calculator.calculate_theoretical_energy_for_circuit(circuit)
        actual_energy = calculator.calculate_actual_energy_for_circuit(circuit)
        return reynolds_number, flow, heights_losses, frictions_losses, theoretical_energy, actual_energy

    # Legacy atm
    def base_study(self, circuit: cir.Circuit):  # pragma: no cover
        for i in range(1, 5 + 1):
            self.velocity_of_medium = i
            print(f"Study with velocity = {self.velocity_of_medium}")
            print(f"Circuit with varying efficiency: \n{self._stepper_range(circuit, 'efficiency', 1, 0.1, 10)[0]}\n")
            print(f"Circuit with varying inside_diameter: "
                  f"\n{self._stepper_range(circuit, 'inside_diameter', 0.1, 1, 10)[0]}\n")
            print(f"Circuit with varying height: \n{self._stepper_range(circuit, 'height', 2, 10, 9)[0]}\n")
            print(f"Circuit with varying Valve settings: \n{self._stepper_boolean(circuit, 'Valve')[0]}\n")
            print(f"Circuit with varying Filter settings: \n{self._stepper_boolean(circuit, 'Filter')[0]}\n")

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

    def _stepper_boolean(self, circuit: cir.Circuit, type_) -> dict:
        if type_ == "Valve":
            attribute = "openness"
            return self._stepper_type(circuit, type_, attribute)
        elif type_ == "Filter":
            attribute = "cleanliness"
            return self._stepper_type(circuit, type_, attribute)
        else:
            raise Exception(f"Invalid type, expected Valve, or Filter, given {type_}")

    # Uses eval, should only be run when tested type_
    def _stepper_type(self, circuit: cir.Circuit, type_, attribute: str) -> dict:
        """
        Takes in a circuit and changes the valves or filters to give different results.

        :param circuit: Circuit to analyze
        :param type_: String with value "Valve" or "Filter"
        :param attribute: Attribute connected to type_ class.
        :return: Dictionary of energy_consumptions. Key is attribute status.
        """
        energy_consumptions = []
        parts_count = 0
        with circuit as test_circuit:
            # Normalize circuit
            for part in test_circuit.canvas:
                if isinstance(part, eval("cir." + type_)):
                    setattr(part, attribute, True)
                    parts_count += 1

            # attributes_matrix = [ [1]*parts_count ] * (parts_count+1)
            # Create a matrix to represent the changed types. All should be true for first round.
            attributes_matrix = []
            for i in range(parts_count + 1):
                attributes_matrix.append([1] * parts_count)
            i = 1
            self._append_energy_consumption(test_circuit, energy_consumptions)

            # Goes through parts and sets one by one to false and appends. Also appends to attributes
            for part in test_circuit.canvas:
                if isinstance(part, eval("cir." + type_)):
                    for j in range(i, parts_count + 1):
                        attributes_matrix[j][i - 1] = 0
                    setattr(part, attribute, False)
                    self._append_energy_consumption(test_circuit, energy_consumptions)
                    i += 1

        attributes_matrix = tuple(tuple(attribute_list) for attribute_list in attributes_matrix)
        dictionary = dict(zip(attributes_matrix, energy_consumptions))
        return dictionary

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
        label = f"Velocity = {str(self.velocity_of_medium)} [m/s]"
        if type_ == "inside_diameter":
            y_values, x_values = self._stepper_range(circuit, type_, start, stop, steps)
            self._plot_image_generator(x_values, y_values, f"Increasing inside diameter [mm]"
                                       , "Energy consumption [kW]", f"Study inside diameter", file_name, label=label)

        elif type_ == "efficiency":
            y_values, x_values = self._stepper_range(circuit, type_, start, stop, steps)
            self._plot_image_generator(x_values, y_values, f"Decreasing efficiency", "Energy consumption [kW]",
                                       f"Study efficiency", file_name, label=label)

        elif type_ == "height":
            y_values, x_values = self._stepper_range(circuit, type_, start, stop, steps)
            self._plot_image_generator(x_values, y_values, f"Increasing height [m]", "Energy consumption [kW]",
                                       f"Study height", file_name, label=label)

    @staticmethod
    def _plot_image_generator(x_values, y_values, x_label, y_label, title, file_name, label=""):
        plt.plot(x_values, y_values, label=label)
        plt.title(title)
        plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        path = pf.PathFinder.get_folder_path("templates")
        file_path = f"{path}/{file_name}"
        plt.savefig(file_path)
        return file_name
