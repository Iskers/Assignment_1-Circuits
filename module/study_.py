from pytypes import typechecked
import numpy as np
import module.circuit as cir
import module.circuit_calculator as calc


class Study:
    def __init__(self):
        self._velocity_of_medium = 5

    @property
    def velocity_of_medium(self):
        return self._velocity_of_medium

    @velocity_of_medium.setter
    def velocity_of_medium(self, value):
        self._velocity_of_medium = value

    def base_study(self, circuit: cir.Circuit):
        for i in range(1, 5):
            self.velocity_of_medium = i
            print(f"Study with velocity = {self.velocity_of_medium}")
            print(f"Circuit with varying efficiency: \n{self._stepper_range(circuit, 'efficiency', 1, 0.1, 10)}\n")
            print(f"Circuit with varying inside_diameter: \n{self._stepper_range(circuit, 'inside_diameter', 0.1, 1, 10)}\n")
            print(f"Circuit with varying height: \n{self._stepper_range(circuit, 'height', 2, 10, 9)}\n")
            print(f"Circuit with varying Valve settings: \n{self._stepper_bool(circuit, 'Valve')}\n")
            print(f"Circuit with varying Filter settings: \n{self._stepper_bool(circuit, 'Filter')}\n")

    def _stepper_range(self, circuit, type_, start: float, stop: float, step: int):
        energy_consumptions = []
        list_ = np.linspace(start, stop, step)
        with circuit as circuit:
            if type_ == "height":
                for i in range(len(list_)):
                    self._canvas_height_adapt(circuit, list_[i])
                    self._append_energy_consumption(circuit, energy_consumptions)
            else:
                for i in range(len(list_)):
                    setattr(circuit, type_, list_[i])
                    self._append_energy_consumption(circuit, energy_consumptions)
        return energy_consumptions

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
        energy_consumptions = []

        with circuit as circuit:
            for part in circuit.canvas:
                if isinstance(part, eval("cir." + type_)):
                    setattr(part, attribute, True)

            self._append_energy_consumption(circuit, energy_consumptions)
            for part in circuit.canvas:
                if isinstance(part, eval("cir." + type_)):
                    setattr(part, attribute, False)
                    self._append_energy_consumption(circuit, energy_consumptions)
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
                            f" fundamenlaly changes the circut. This requires removing all bends and content between. "
                            f"Height of circuit is {circuit.height}")

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
                            return circuit.height
            raise Exception(f"Not allowed to remove {height} from {circuit}")

        elif circuit.height < height:
            pipe = cir.PipeStraight("Added_pipe", circuit.inside_diameter, delta, 90)
            self._add_parts_to_canvas(circuit, pipe)
            return circuit.height

    # TODO expand for more parts
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
