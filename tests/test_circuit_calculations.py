# noinspection PyUnboundLocalVariable
if __name__ == "__main__" and __package__ is None:  # pragma: no cover
    __package__ = "package.tests"

import unittest
import module.circuit_calculator as calc
import module.circuit as cir
import module.parsers as par


class CircuitCalculatorTester(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = par.Parser()
        self.calculator = calc.CircuitCalculator()
        self.circuit_default_example = self.parser.pars("circuit.tsv", format_="tsv", true_path=False)

    def test_main_case_calculation(self):
        self.calculator.calculate_actual_energy_for_circuit(self.circuit_default_example)

    def test_formulas_existence(self):
        self.assertIsInstance(self.calculator.circuit_formulas, calc.CircuitFormulas)


class CircuitFormulasTester(unittest.TestCase):
    def setUp(self) -> None:
        self.circuit_formulas = calc.CircuitFormulas()

    def test_area(self):
        diameter = 4
        area_with_4_diameter = 12.57
        self.assertEqual(round(calc.CircuitFormulas.calculate_area(diameter), 2), area_with_4_diameter
                         , f"Should be {area_with_4_diameter}")

    def test_calculate_delta_height(self):
        height = 10
        delta_height_10m = 100552.5
        self.assertEqual(round(calc.CircuitFormulas.calculate_delta_height(height, 9.81, 1025), 2), delta_height_10m
                         , f"Should be {delta_height_10m}")

    def test_ZETA_for_parts_and_changing_some_values(self):
        bend = cir.PipeBend("Some_bend", 0.1)
        valve = cir.Valve("Some_valve", True)
        filter_ = cir.Filter("Some_filter", True)

        self.assertEqual(calc.CircuitFormulas.calculate_zeta_bend(), bend.ZETA)
        self.assertEqual(calc.CircuitFormulas.calculate_zeta_valve(True), valve.ZETA)
        self.assertEqual(calc.CircuitFormulas.calculate_zeta_filter(True), filter_.ZETA)

        valve.openness = False
        filter_.cleanliness = False

        self.assertEqual(calc.CircuitFormulas.calculate_zeta_valve(False), valve.ZETA)
        self.assertEqual(calc.CircuitFormulas.calculate_zeta_filter(False), filter_.ZETA)

    def test_flow_calculation(self):
        area = 10
        velocity = 10
        self.assertEqual(calc.CircuitFormulas.calculate_flow(area, velocity), area * velocity,
                         f"Should be {area * velocity}")

    # TODO finish tests
    def est_calculate_losses_of_pressure(self):
        calculator = calc.CircuitCalculator()
        calc.CircuitFormulas.calculate_losses_of_pressure(density_of_medium=calculator.DENCITY_OF_SEAWATER)
        pass

    def test_calculate_flow_coefficient(self):
        self.assertEqual(round(calc.CircuitFormulas.calculate_flow_coefficient(2400), 4), 0.0451)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
