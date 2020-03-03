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

    # CLASS SPESIFIC HTML METHODS
    def serialize_circuit(self, circuit):
        result = self._serialize_open_tag("")

    def serialize_list_of_energy_consumptions(self, list_: list):
        return HTMLContext.table_data(self, list_)


class PageGenerator:
    def __init__(self, template_file, target_file, **kwargs):
        self._template_file = template_file
        self._target_file = target_file
        self.render_study(self.template_file, self.target_file)

    @property
    def template_file(self):
        return self._template_file

    @property
    def target_file(self):
        return self._target_file

    @staticmethod
    def render_study(template_file, target_file):
        study_instance = study.Study()

        with fh.File(template_file, "r") as template:
            for line in template:
                line = line.rstrip()

        with fh.File(target_file, "w") as target:
            pass

    # TODO remove
    @staticmethod
    def render_page(template_loc, file_name, **kwargs):
        return jinja.Environment(loader=jinja.FileSystemLoader(template_loc)). \
            get_template(file_name).render(kwargs)
