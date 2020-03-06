import unittest
from module import circuit as cir


class CircuitClassTester(unittest.TestCase):
    """
    Includes tests for both circuit and parts.
    """

    # TODO move example_circuit here ?
    def setUp(self) -> None:
        pass

    @staticmethod
    def example_circuit() -> cir.Circuit:
        circuit = cir.Circuit()
        circuit.add_tank("TI")
        circuit.add_straight_pipe("P1", 0.32, 10, 0)
        circuit.add_pump("Pu1", 0.76)
        circuit.add_straight_pipe("P2", 0.32, 10, 0)
        circuit.add_valve("V1", False)
        circuit.add_bend_pipe("B1", 0.32)
        circuit.add_straight_pipe("P3", 0.32, 6, 90)
        circuit.add_valve("V2", True)
        circuit.add_bend_pipe("B2", 0.32)
        circuit.add_straight_pipe("P4", 0.32, 10, 0)
        circuit.add_filter("F1", True)
        circuit.add_straight_pipe("P5", 0.32, 10, 0)
        circuit.add_tank("TE")
        circuit.name = "Some_name"
        return circuit

    def test__init__(self):
        circuit = cir.Circuit()
        self.assertEqual(circuit.canvas, [])
        self.assertTrue(circuit._validness)
        self.assertIsNone(circuit._height)
        self.assertEqual(circuit._inside_diameter, 0.0)
        # Extra for good measure
        self.assertIs(type(circuit._inside_diameter), float)
        self.assertIsInstance(circuit.canvas, list)

    def test__getitem__(self):
        circuit = self.example_circuit()
        part = circuit[1]
        self.assertIsInstance(part, cir.PipeStraight)

    def test_get_set_name(self):
        circuit = self.example_circuit()
        self.assertEqual(circuit.name, "Some_name")
        circuit.name = "SomeOtherName"
        self.assertEqual(circuit.name, "SomeOtherName")

    def test_get_set_height(self):
        circuit = self.example_circuit()
        self.assertEqual(circuit.height, 6, "Should be 6")
        with self.assertRaises(Exception):
            circuit.height = 0

    def test_get_set_inside_diameter(self):
        circuit = self.example_circuit()
        self.assertEqual(circuit.inside_diameter, 0.32, "Should be 0.32")
        circuit.inside_diameter = 12
        self.assertEqual(circuit.inside_diameter, 12)

    def test_get_set_efficiency_of_pump(self):
        circuit = self.example_circuit()
        self.assertEqual(circuit.efficiency, 0.76, "Should be 0.76")
        circuit.efficiency = 0.5
        self.assertEqual(circuit.efficiency, 0.5)
        with self.assertRaises(Exception):
            circuit.efficiency = 100

    def test_add_part(self):
        circuit = cir.Circuit()
        part_pipe_list_str = ["pipe", "Pipe_name_tester", "6", "0.1", "0"]
        circuit.add_part_from_string(part_pipe_list_str)
        self.assertIsInstance(circuit[0], cir.PipeStraight)

    # TODO Add testers for more parts

    def test_get_attribute(self):
        circuit = self.example_circuit()

        for attr, value in circuit[1].__dict__.items():
            print(attr, value)

        for property_, value in vars(circuit[1]).items():
            print(property_, value)

        for property_ in dir(circuit[1]):
            if not property_.startswith('_'):
                print(property_)
