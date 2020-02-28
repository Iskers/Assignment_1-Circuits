from unittest import TestCase
import module.page_gen as pgen
import module.path_finder as pf
import module.file_handler as fh
import module.study_ as stdy
import tests.test_circuit as tst_cir


class TestPageGenerator(TestCase):
    def setUp(self) -> None:
        self.template_file = pf.PathFinder.get_file_path("study-template.html", "templates")
        self.target_file = pf.PathFinder.get_file_path("study.html", "data")

    def tearDown(self) -> None:
        self.template_file = None
        self.target_file = None

    def test_render_study(self):
        page = pgen.PageGenerator(self.template_file, self.target_file)


class TestStudyHTMLSerializer(TestCase):
    def test_serialize_circuit(self):
        pass

    def test_serialize_list_of_energy_consumption(self):
        target_file = pf.PathFinder.get_file_path("study.html", "data")
        gen = pgen.StudyHTMLSerializer()
        study = stdy.Study()
        circuit = tst_cir.CircuitClassTester.example_circuit()
        list_ = study._stepper_range(circuit, 'efficiency', 1, 0.1, 10)

        string = gen.serialize_list_of_energy_consumptions(list_)
        with fh.File(target_file, "w") as target_file:
            target_file.write(string)

        print(string)

    def test_table_header(self):
        list_ = ["first", "second", "third"]
        gen = pgen.StudyHTMLSerializer()
        string = pgen.HTMLContext.table_header(gen, list_)
        print(string)
