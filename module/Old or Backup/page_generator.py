import re
import module.file_handler as fh
import module.study_ as study


class HTMLSerializer:
    def __init__(self, indentation="\t"):
        self._indentation = indentation
        self._depth = 0

    # GETTERS AND SETTERS
    @property
    def indentation(self):
        return self._indentation

    @indentation.setter
    def indentation(self, value):
        self._indentation = value

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    # SERIALIZERS
    @staticmethod
    def _serialize_open_tag(name):
        return "<" + name + ">\n"

    @staticmethod
    def _serialize_close_tag(name):
        return "</" + name + ">\n"


class HTMLContext(HTMLSerializer):
    def __init__(self, html_serializer: HTMLSerializer, tag: str):
        super().__init__(html_serializer.indentation)
        self._indentation = html_serializer.indentation
        self._depth = html_serializer.depth
        self._tag = tag
        self._line = ""

    # OVERLOADS
    def __iadd__(self, other):
        self.line += other
        return self

    # CONTEXT DEFINITION
    def __enter__(self):
        self.line += self._serialize_open_tag(self.tag)
        self.depth += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.depth -= 1
        self.line += self._serialize_close_tag(self.tag)

    # SETTERS AND GETTERS
    @property
    def tag(self):
        return self._tag

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    # HTML METHODS
    # GENERAL METHODS
    @staticmethod
    def paragraph(html_serializer: HTMLSerializer, package: str):
        with HTMLContext(html_serializer, "p") as context:
            context += package
        return context.line

    @staticmethod
    def table_row(html_serializer: HTMLSerializer, package: str):
        with HTMLContext(html_serializer, "tr") as row:
            row += package
        return row.line

    @staticmethod
    def table_single_header(html_serializer: HTMLSerializer, package: str):
        with HTMLContext(html_serializer, "th") as header:
            header += package
        return header.line

    @staticmethod
    def table_item(html_serializer: HTMLSerializer, package: str):
        with HTMLContext(html_serializer, "td") as table_data:
            table_data += package
        return table_data.line

    # COMPOSED METHODS
    @classmethod
    def table(cls, header_list, data_list: list):
        result = "<table>"
        result += cls.table_header(cls, header_list)
        result += cls.table_data(cls, data_list)
        result += "<table/>"
        return result

    @staticmethod
    def table_header(html_serializer: HTMLSerializer, list_: list):
        complete_header = ""
        for header in list_:
            header += "\n"
            complete_header += HTMLContext.table_single_header(html_serializer, header)
        return HTMLContext.table_row(html_serializer, complete_header)

    @staticmethod
    def table_data(html_serializer: HTMLSerializer, list_: list, separator=","):
        complete_data = ""
        for data in list_:
            data = str(data)
            if data is not list_[-1]:
                data += separator + "\n"
                complete_data += HTMLContext.table_item(html_serializer, data)
        return HTMLContext.table_row(html_serializer, complete_data)


class StudyHTMLSerializer(HTMLSerializer):
    def __init__(self):
        super().__init__()
        self.study = study.Study()

    # CLASS SPECIFIC HTML METHODS
    def serialize_circuit(self, circuit) -> str:
        result = self._serialize_open_tag("")
        return result

    def serialize_table(self, title, header_list, data_list):
        HTMLContext.table(self, header_list, data_list)

    def serialize_list_of_energy_consumptions(self, list_: list):
        return HTMLContext.table_data(self, list_)


class PageGenerator:
    def __init__(self, template_file, target_file, **kwargs):
        self._template_file = template_file
        self._target_file = target_file
        self.study_serializer = StudyHTMLSerializer()
        self.render_study(self.template_file, self.target_file)

    @property
    def template_file(self):
        return self._template_file

    @property
    def target_file(self):
        return self._target_file

    def render_study(self, circuit, template_file, target_file):
        with fh.File(template_file, "r") as template:
            with fh.File(target_file, "w") as target:
                for line in template:
                    line = self.HTML_replacement(circuit, line)
                    target.write(line + '\n')

    def serialize_circuit(self, circuit) -> str:

        pass

    def HTML_replacement(self, circuit, line: str):
        line = line.rstrip()
        # Methods to be called to replace placeholder in template with some value.
        methods = {r'__Circuit__': lambda: re.sub(r'__Circuit__',
                                                  self.study_serializer.serialize_circuit(circuit), line),
                   r'__base_study__': lambda: re.sub(r'__base_study__', self.study_serializer
                                                     .serialize_circuit(circuit), line)}
        for key in methods:
            if re.search(key, line):
                return methods[key]
        return line
