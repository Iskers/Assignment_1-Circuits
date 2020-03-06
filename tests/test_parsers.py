# noinspection PyUnboundLocalVariable
from unittest import TestCase

if __name__ == "__main__" and __package__ is None:  # pragma: no cover
    __package__ = "package.tests"

import pathlib
import unittest
import module.circuit as cir
import module.parsers as par

file_name1 = pathlib.Path(__file__).parent
file_name1 = file_name1.parent / 'data' / 'circuit.tsv'

file_name2 = pathlib.Path(__file__).parent
file_name2 = file_name2.parent / 'data' / 'circuit.xml'


class ParserClassTester(unittest.TestCase):
    """
    Uses unittest to tests all member functions of the class Parser Class.
    setUp() initializes each tests function instance, and tearDown() is called as a
    destructor after the tests function is run.
    In this way each tests has a fresh parser and circuit.
    """

    def setUp(self) -> None:
        self.parser = par.Parser()
        self.circuit = cir.Circuit()

    def tearDown(self) -> None:
        self.parser = None
        self.circuit = None

    ''' Should only be run when testing file_handler.py as it throws sys.exit()
    def test_file_error_throw(self):
        #self.assertRaises(OSError, lambda: with fh.File("Some/random/path", "r") as file_source: pass)
        with fh.File("Some/random/path", "r") as file_source:
            pass
    '''

    def test_parse(self):
        with self.assertRaises(Exception):
            self.parser.parse(file_name="circuit.xml", true_path=False, format_="random_format")

    def test_xml(self):
        circuit = self.parser.parse(file_name="circuit.xml", true_path=False, format_="xml")
        pass

    def test_separator(self):
        self.parser.separator = " "
