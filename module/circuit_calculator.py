import math
import warnings
import module.circuit as cir


class CircuitFormulas:
    def __init__(self):
        pass

    @staticmethod
    def calculate_actual_energy(theoretical_energy: float, efficiency_of_pump: float) -> float:
        return theoretical_energy / efficiency_of_pump

    @staticmethod
    def calculate_theoretical_energy(pressure_losses_due_height: float, pressure_losses_due_to_friction: float,
                                     flow: float) -> float:
        return ((pressure_losses_due_height + pressure_losses_due_to_friction) * flow) / 1000

    @staticmethod
    def calculate_pressure_losses_from_height(height: float, gravitational_constant: float = 9.81,
                                              density_of_medium: int = 1025) -> float:
        return height * gravitational_constant * density_of_medium

    @staticmethod
    def calculate_losses_of_pressure_in_pipe(flow_coefficient: int, inside_diameter: float, density_of_medium: int,
                                             velocity_of_medium: float) -> float:
        return flow_coefficient * (1 / inside_diameter) * (density_of_medium / 2) * velocity_of_medium

    @staticmethod
    def calculate_reynolds_number(velocity_of_medium: float, inside_diameter: float,
                                  kinematic_viscosity_of_medium: float = 1.35 * 10 ** -6) -> float:
        return (velocity_of_medium * inside_diameter) / kinematic_viscosity_of_medium

    @staticmethod
    def calculate_flow_coefficient(reynolds_number: float) -> float:
        # Disable reynolds warning if necessary
        if reynolds_number > 10**5:
            warnings.warn("Reynolds number exceeding 10^5")
        if reynolds_number < 2300:
            return 64 / reynolds_number
        else:
            return 0.316 / reynolds_number ** (1 / 4)

    @staticmethod
    def calculate_losses_of_pressure_other(density_of_medium: int, velocity_of_medium: float, zeta: float) -> float:
        return zeta * density_of_medium / 2 * velocity_of_medium ** 2

    @staticmethod
    def calculate_flow(area: float, velocity: float) -> float:
        return area * velocity

    @staticmethod
    def calculate_area(diameter: float) -> float:
        return (math.pi * diameter ** 2) / 4

    # Used for testing
    @staticmethod
    def calculate_zeta_bend() -> float:
        return 0.1 * math.sin(math.pi / 2)

    @staticmethod
    def calculate_zeta_valve(openness: bool) -> float:
        if openness:
            return 0.2
        else:
            return 4

    @staticmethod
    def calculate_zeta_filter(cleanliness: bool) -> float:
        if cleanliness:
            return 0.5
        else:
            return 5


class CircuitCalculator:
    # Formulas
    circuit_formulas = CircuitFormulas()

    # Constants
    DENSITY_OF_SEAWATER = 1025  # [kg/m^3]
    GRAVITATIONAL_CONSTANT = 9.81  # [m/s^2]
    KINEMATIC_VISCOSITY_OF_SEAWATER = 1.35 * 10 ** (-6)  # [m/s^2]

    # Variables
    _velocity_of_medium: float  # [m/s]

    def __init__(self, velocity_of_medium: float = 5):
        self._velocity_of_medium = velocity_of_medium

    def calculate_core_attributes(self, circuit: cir.Circuit):
        area = self.circuit_formulas.calculate_area(circuit.inside_diameter)
        reynolds_number = self.calculate_reynolds_number(circuit)
        flow_coefficient = self.circuit_formulas.calculate_flow_coefficient(reynolds_number)
        flow_of_seawater = self.circuit_formulas.calculate_flow(area, self._velocity_of_medium)
        pressure_losses_from_height = self.calculate_losses_from_height(circuit)
        pressure_losses_from_frictions = self.calculate_losses_from_frictions(circuit, flow_coefficient)
        return pressure_losses_from_height, pressure_losses_from_frictions, flow_of_seawater

    def calculate_losses_from_frictions(self, circuit: cir.Circuit, flow_coefficient):
        pressure_losses_from_frictions = 0
        for part in circuit:
            pressure_losses_from_frictions += part.calculate_losses_of_pressure(self.DENSITY_OF_SEAWATER
                                                                                , self._velocity_of_medium
                                                                                , flow_coefficient)
        return pressure_losses_from_frictions

    def calculate_losses_from_height(self, circuit: cir.Circuit) -> float:
        return self.circuit_formulas.calculate_pressure_losses_from_height(circuit.height, self.GRAVITATIONAL_CONSTANT,
                                                                           self.DENSITY_OF_SEAWATER)

    def calculate_reynolds_number(self, circuit):
        return self.circuit_formulas.calculate_reynolds_number(self._velocity_of_medium,
                                                                circuit.inside_diameter,
                                                                self.KINEMATIC_VISCOSITY_OF_SEAWATER)

    def calculate_theoretical_energy_for_circuit(self, circuit: cir.Circuit):
        delta_height, delta_frictions, flow = self.calculate_core_attributes(circuit)
        theoretical_energy = self.circuit_formulas.calculate_theoretical_energy(delta_height, delta_frictions, flow)
        return theoretical_energy

    def calculate_actual_energy_for_circuit(self, circuit: cir.Circuit):
        theoretical_energy = self.calculate_theoretical_energy_for_circuit(circuit)
        actual_energy = self.circuit_formulas.calculate_actual_energy(theoretical_energy,
                                                                      circuit.efficiency)
        return actual_energy
