from unittest import TestCase
import module.page_generator as pgen
import module.path_finder as pf
import module.file_handler as fh
import module.study_ as stdy
import tests.test_circuit as tst_cir

'''
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
'''


class TestHTMLSerializer(TestCase):
    def setUp(self) -> None:
        self.html_serializer = pgen.HTMLSerializer()
        self.circuit = tst_cir.CircuitClassTester.example_circuit()
        self.html_creator = pgen.HTMLPageGenerator()

    def tearDown(self) -> None:
        self.html_serializer = None
        self.circuit = None
        self.html_creator = None

    def test_serialize_circuit(self):
        self.html_serializer.serialize_circuit(self.circuit)

    def test_serialize_circuit_attributes(self):
        self.html_serializer.serialize_circuit_attributes(self.circuit)


class TestHTMLCreator(TestCase):
    def setUp(self) -> None:
        self.circuit = tst_cir.CircuitClassTester.example_circuit()
        self.html_creator = pgen.HTMLPageGenerator()

    def tearDown(self) -> None:
        self.circuit = None
        self.html_creator = None

    def test_export_circuit_study_in_html(self):
        self.html_creator.export_circuit_study_in_HTML(self.circuit, "study-template.html", "study.html")

    def test_print_report(self):
        pass

    def test_html_replacement(self):
        pass

    def test_serialize_img_study(self):
        print(self.html_creator.print_img(self.circuit))

    def test_print_boolean_study(self):
        print(self.html_creator.print_boolean_study(self.circuit))