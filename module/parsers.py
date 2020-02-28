import module.circuit as cir
import module.file_handler as fh
import module.path_finder as pf
import xml.etree.ElementTree as et


class Parser:
    """
    This is a class for parsing text in the tsv, csv, and xml formats using a file handler.

    Attributes\:
        Separator: Separator for the parsing text, default is tabulation.

    """

    def __init__(self, separator: str = '\t'):
        """
        The constructor for Parser class.

        :rtype: object
        :param separator:
        """
        self._separator = separator
        pass

    @property
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, separator):
        self._separator = separator

    def pars(self, file_name: str, format_, true_path: bool = True, circuit: cir.Circuit = None) -> cir.Circuit:
        if not circuit:
            circuit = cir.Circuit()
        if not true_path:
            file_name = pf.PathFinder.get_file_path(file_name=file_name, folder_name="data")

        with fh.File(file_name, "r") as file_source:
            if format_ == "tsv":
                return self._tsv_parser(file_source, circuit)
            elif format_ == "xml":
                return self._xml_parser(file_source, circuit)
            else:
                raise Exception("Invalid format")

    def _tsv_parser(self, file_source, circuit: cir.Circuit) -> cir.Circuit:
        """
        Takes inn a file and appends it to a given circuit. If the file is in the data folder the filename can be given
        only with the name of the file.

        :param file_source: Source file
        :param circuit: Given circuit to append
        :return: Appended circuit
        :rtype cir.Circuit:
        """
        header = file_source.readline()
        header = self._line_treatment(header, self.separator)

        for line in file_source:
            if "end\n" in line:
                break
            else:
                self._tsv_line_parser(line, circuit)

        circuit.name = header[1]
        return circuit

    def _tsv_line_parser(self, line: str, circuit: cir.Circuit):
        """Takes a line and appends it to a ciruit"""
        line = self._line_treatment(line, self.separator)
        circuit.add_part_from_string(line)

    @staticmethod
    def _line_treatment(line: str, separator) -> list:
        line = line.rstrip()
        list_ = line.split(separator)
        return list_

    def _xml_parser(self, file_source, circuit: cir.Circuit) -> cir.Circuit:
        xml_document = self._xml_document_loader(file_source)
        root = xml_document.getroot()
        circuit.name = root.attrib["name"]

        for child in root:
            type_ = child.tag
            part = cir.Part.factory_function(type_=type_, **child.attrib)
            circuit.add_part(part)

        return circuit

    @staticmethod
    def _xml_document_loader(file_source) -> et.ElementTree:
        xml_document = et.parse(file_source)
        return xml_document
