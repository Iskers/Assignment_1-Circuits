from unittest import TestCase
import module.study_ as stdy
import module.parsers as pars


class TestStudy(TestCase):
    def test_base_study(self):
        parser = pars.Parser()
        study = stdy.Study()
        circuit = parser.parse("task_circuit.tsv", format_="tsv", true_path=False)
        # study.base_study(circuit)

    def test__canvas_height_adapt(self):
        parser = pars.Parser()
        study = stdy.Study()
        circuit = parser.parse("task_circuit.tsv", format_="tsv", true_path=False)
        study._canvas_height_adapt(circuit, 10)
        self.assertRaises(Exception, lambda: study._canvas_height_adapt(circuit, 0.5))
