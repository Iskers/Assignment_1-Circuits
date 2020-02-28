import re
import package.module.file_handler as fh
import package.module.study_ as study


class HTMLSerializer:
    def __init__(self, indentation="\t"):
        self._indentation = indentation
        self._depth = 0

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

    def _serialize_indentation(self):
        result = ""
        for de in range(0, self.depth):
            result += self.indentation
        return result

    def _serialize_open_tag(self, name):
        return self._serialize_indentation() + "<" + name + ">\n"

    def _serialize_close_tag(self, name):
        return self._serialize_indentation() + "</" + name + ">\n"


class HTMLContext(HTMLSerializer):
    def __init__(self, html_serializer: HTMLSerializer, tag: str):
        super().__init__(html_serializer.indentation)
        self._indentation = html_serializer.indentation
        self._depth = html_serializer.depth
        self._tag = tag
        self._line = ""

    def __iadd__(self, other):
        self.line += self._serialize_indentation()
        self.line += other
        return self

    def __enter__(self):
        self.line += self._serialize_open_tag(self.tag)
        self.depth += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.depth -= 1
        self.line += self._serialize_close_tag(self.tag)

    @property
    def tag(self):
        return self._tag

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    def _serialize_open_tag(self, name):
        return "<" + name + ">\n"

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
    def table_header(html_serializer: HTMLSerializer, list_: list):
        complete_header = ""
        for header in list_:
            header += "\n"
            complete_header += HTMLContext.table_single_header(html_serializer, header)
        return HTMLContext.table_row(html_serializer, complete_header)


class StudyHTMLSerializer(HTMLSerializer):
    def __init__(self):
        super().__init__()
        self.study = study.Study()

    def serialize_circuit(self, circuit):
        result = self._serialize_open_tag("")

    def serialize_list_of_energy_consumptions(self, list_: list):
        HTMLContext.html_in_context(self, table)


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

    @staticmethod
    def render_page(template_loc, file_name, **kwargs):
        return jinja.Environment(loader=jinja.FileSystemLoader(template_loc)). \
            get_template(file_name).render(kwargs)
