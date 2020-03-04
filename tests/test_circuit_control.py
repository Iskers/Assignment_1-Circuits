import unittest
import module.circuit_control as circ
import module.circuit as cir
import module.parsers as pars


class CircuitControlTester(unittest.TestCase):
    """
    Uses the invalid and valid circuits in data to show that errors are correctly thrown.
    """
    # UTILITIES
    def setUp(self) -> None:
        self.circuit = cir.Circuit()
        self.parser = pars.Parser()
        self.controller = circ.CircuitControl()

    def tearDown(self) -> None:
        self.circuit = None
        self.parser = None
        self.controller = None

    def tsv_standard(self, file_name: str) -> cir.Circuit:
        return self.parser.parse(file_name, format_="tsv", true_path=False)

    def faulty_circuits_control(self, circuit: cir.Circuit):
        try:
            self.controller.control_circuit(circuit)
        except Exception as failure:
            print(f"This circuit, {circuit}, has a fault: \n{failure}")

    def standard_faulty_method(self, circuit_name: str):
        self.circuit = self.tsv_standard(circuit_name)
        print("\n" + circuit_name)
        self.faulty_circuits_control(self.circuit)

    # todo remove these methods
    # ACTUAL TSV TESTS
    # First alternative with lambda function
    def test_tsp_invalid_circuit1_with_lambda_method(self):
        self.circuit = self.tsv_standard("invalid_circuit1.tsv")
        self.assertRaises(Exception, lambda: self.controller.control_circuit(self.circuit))

    # Second alternative with context manager
    def test_tsc_invalid_circuit2_with_context_manager(self):
        self.circuit = self.tsv_standard("invalid_circuit2.tsv")
        with self.assertRaises(Exception) as excep:
            self.controller.control_circuit(self.circuit)


class StandardCircuitTester(CircuitControlTester):
    def setUp(self) -> None:
        self.circuit = cir.Circuit()
        self.parser = pars.Parser()
        self.controller = circ.CircuitControl()

    def tearDown(self) -> None:
        self.circuit = None
        self.parser = None
        self.controller = None

    # Test of original circuit
    def test_tsv_standard(self):
        self.circuit = self.tsv_standard("circuit.tsv")
        self.assertTrue(self.controller.control_circuit(self.circuit))

    def test_tsv_valid_circuit2(self):
        self.circuit = self.tsv_standard("valid_circuit1.tsv")
        self.assertTrue(self.controller.control_circuit(self.circuit))


class InvalidCircuitTester(CircuitControlTester):
    # Testing with the standard testing method
    def test_tsv_invalid_circuit1(self):
        self.standard_faulty_method("invalid_circuit1.tsv")

    def test_tsv_invalid_circuit2(self):
        self.standard_faulty_method("invalid_circuit2.tsv")

    def test_tsv_invalid_circuit3(self):
        self.standard_faulty_method("invalid_circuit3.tsv")

    def test_tsv_invalid_circuit4(self):
        self.standard_faulty_method("invalid_circuit4.tsv")

    def test_tsv_invalid_circuit5(self):
        self.standard_faulty_method("invalid_circuit5.tsv")

    def test_tsv_invalid_circuit6(self):
        self.standard_faulty_method("invalid_circuit6.tsv")

    def test_tsv_invalid_circuit7(self):
        self.standard_faulty_method("invalid_circuit7.tsv")

    def test_tsv_invalid_circuit8(self):
        self.standard_faulty_method("invalid_circuit8.tsv")

    def test_tsv_invalid_circuit9(self):
        self.standard_faulty_method("invalid_circuit9.tsv")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
