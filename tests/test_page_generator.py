from unittest import TestCase
import module.page_generator as pgen
import module.study_ as stdy
import tests.test_circuit as tst_cir


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

    # Not to be run as it interferes with printing
    def test_serialize_img_study(self):
        # self.assertIsNotNone(self.html_creator.print_img(self.circuit))
        pass

    def test_print_boolean_study(self):
        self.assertIsNotNone(self.html_creator.print_boolean_study(self.circuit))