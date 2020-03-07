import re
import num2words
import module.file_handler as fh
import module.path_finder as pf
import module.study_ as stdy


class HTMLSerializer:
    def __init__(self):
        pass

    def serialize_circuit(self, circuit):
        title = f"<h2>{circuit}</h2>"
        body = ""
        for part in circuit:
            body = self._serialize_message("li", str(part))
        body = self._serialize_message("ul", body)
        return title + body

    def serialize_circuit_with_attributes(self, circuit):
        title = f"<h2>{self._sting_treatment(str(circuit))}</h2>"
        body = self._serialize_message("th", "Types: ")
        for part in circuit:
            if type(part).__name__ == "PipeStraight":
                body += self._serialize_message("th", "Pipe")
            elif type(part).__name__ == "PipeBend":
                body += self._serialize_message("th", "Bend")
            else:
                body += self._serialize_message("th", f"{type(part).__name__}")
        body = self._serialize_message("tr", body)

        # Zeta should not be on the circuit representation
        properties = {"ZETA"}

        for part in circuit:
            for evaluation_property, unused_value in vars(part).items():
                if evaluation_property not in properties:
                    property_print = self._sting_treatment(evaluation_property[1:])
                    inner_body = self._serialize_message_with_options("td", property_print, "id=\"property\"")
                    for inner_part in circuit:
                        if evaluation_property not in vars(inner_part):
                            inner_body += self._serialize_message_with_options("td", "", "id=\"empty_item_property\"")
                        else:
                            for item_property, value in vars(inner_part).items():
                                if item_property == evaluation_property:
                                    inner_body += self._serialize_message_with_options("td", value,
                                                                                       "id=\"item_property\"")
                    properties.add(evaluation_property)
                    body += self._serialize_message("tr", inner_body)

        body = self._serialize_message_with_options("table", body, "id=\"circuit\"")
        return title + body

    def serialize_img_study(self, circuit, study, v_range, d_range, e_range, h_range):
        file_names = study.png_generator_plot(circuit, v_range, d_range, e_range, h_range)
        title = self._serialize_message("h2", "Plots of differing attributes and their effect on energy consumption")
        body = ""
        for file in file_names:
            body += self._serialize_image(file)
        body = self._serialize_message_with_options("div", body, "id=\"image_study\"")
        return title + body

    def serialize_all_boolean_studies(self, circuit, study_):
        title = self._serialize_message("h2", "Boolean study")
        valve_study, filter_study, velocities = study_.boolean_study(circuit)

        serialized_valve_string = self._serialize_boolean_study(valve_study, velocities, "Valve", "open")

        serialized_filter_string = self._serialize_boolean_study(filter_study, velocities, "Filter", "clean")

        # tables = self._serialize_message("table", serialized_valve_string + serialized_filter_string)
        tables = serialized_valve_string + serialized_filter_string
        return title + tables

    def serialize_core_attributes(self, circuit, velocity):
        study = stdy.Study(velocity)
        core_attributes = study.circuit_performance(circuit)

        title = self._serialize_message("h3", f"Core attributes of circuit with velocity of {velocity} [m/s]")
        body = self._serialize_message("li", f"Reynolds number = {round(core_attributes[0])}")
        body += self._serialize_message("li", f"Flow = {round(core_attributes[1], 4)} [m3/s]")
        body += self._serialize_message("li", f"Pressure losses due to height of circuit = {round(core_attributes[2])}"
                                              f" [N/m2]")
        body += self._serialize_message("li", f"Pressure losses due to friction in parts = "
                                              f"{round(core_attributes[3])} [N/m2]")
        body += self._serialize_message("li", f"Theoretical energy usage of circuit = {round(core_attributes[4], 2)}"
                                              f" [kW]")
        body += self._serialize_message("li", f"Actual energy usage of circuit = {round(core_attributes[5], 2)} [kW]")
        return title + self._serialize_message("ul", body)

    def _serialize_boolean_study(self, boolean_study, velocities, type_word, keyword: str, ):
        title = self._serialize_message("h3", f"Study of {type_word.lower()} setting at"
                                              f" different velocities")
        # Create table header
        serialized_valve_string = self._serialize_message("th", f"{type_word}s {keyword}: ")
        for key in boolean_study[0]:
            serialized_valve_string += self._serialize_message("th", num2words.num2words(sum(key)))

        serialized_valve_string = self._serialize_message("tr", serialized_valve_string)
        for i in range(len(velocities)):
            serialized_velocity_string = self._serialize_message("td", f"Velocity = {velocities[i]} [m/s]")
            for key in boolean_study[i]:
                serialized_velocity_string += self._serialize_message("td", boolean_study[i][key])
            serialized_valve_string += self._serialize_message("tr", serialized_velocity_string)

        serialized_valve_string = self._serialize_message("table", serialized_valve_string)
        return title + serialized_valve_string

    @staticmethod
    def _serialize_message(tag: str, msg) -> str:
        body = HTMLSerializer._serialize_open_tag(tag)
        body += str(msg)
        body += HTMLSerializer._serialize_close_tag(tag)
        return body

    @staticmethod
    def _serialize_message_with_options(tag: str, msg, option):
        body = HTMLSerializer._serialize_open_tag_with_options(tag, option)
        body += str(msg)
        body += HTMLSerializer._serialize_close_tag(tag)
        return body

    @staticmethod
    def _serialize_open_tag(name):
        return f"<{name}>"

    @staticmethod
    def _serialize_open_tag_with_options(name, option):
        return f"<{name} {option}>"

    @staticmethod
    def _serialize_close_tag(name):
        return f"</{name}>"

    @staticmethod
    def _serialize_image(img_path):
        img_path = img_path.replace(" ", "%20")
        return f"<img src={img_path}>"

    @staticmethod
    def _serialize_image_with_options(img_path, option):
        img_path = img_path.replace(" ", "%20")
        return f"<img src={img_path} {option}>"

    @staticmethod
    def _sting_treatment(string):
        string = string.replace("_", " ")
        string = string.title()
        return string


class HTMLPageGenerator:
    def __init__(self):
        self.serializer = HTMLSerializer()
        self.study = stdy.Study()
        self.path = pf.PathFinder.get_folder_path("templates")

    def default_page_generation(self, circuit, base_velocity=5, velocity_range=(1, 5, 1), diameter_range=(0.1, 1, 10),
                                efficiency_range=(0.1, 1, 10), height_range=(1, 10, 9)):

        self.export_circuit_study_in_HTML(circuit, "study-template.html", "study.html", base_velocity, velocity_range,
                                          diameter_range, efficiency_range, height_range)

    def export_circuit_study_in_HTML(self, circuit, template_file, target_file,
                                     base_velocity=5, velocity_range=(1, 5, 1),
                                     diameter_range=(0.1, 1, 10), efficiency_range=(0.1, 1, 10),
                                     height_range=(1, 10, 9)):
        template_file = str(self.path) + "/" + template_file
        target_file = str(self.path) + "/" + target_file
        with fh.File(template_file, "r") as template:
            with fh.File(target_file, "w") as target:
                self.print_report(circuit, template, target, base_velocity, velocity_range, diameter_range,
                                  efficiency_range, height_range)

    def print_report(self, circuit, template_stream, target_stream, velocity, v_range, d_range,
                     e_range, h_range):
        for line in template_stream:
            line = self.HTML_replacement(circuit, line, velocity, v_range, d_range,
                                         e_range, h_range)
            target_stream.write(line + '\n')

    def HTML_replacement(self, circuit, line: str, velocity, v_range, d_range, e_range, h_range):
        line = line.rstrip()
        # Methods to be called to replace placeholder in template with some value.
        # Lambda takes in two arguments and gives back string.
        methods = {r'__Circuit__': lambda line_, circuit_: re.sub(r'__Circuit__', self.print_circuit(circuit_),
                                                                  line_),
                   r'__core_attr__': lambda line_, circuit_: re.sub(r'__core_attr__',
                                                                    self.print_core_attributes(circuit_, velocity),
                                                                    line_),
                   r'__boolean_study__': lambda line_, circuit_: re.sub(r'__boolean_study__',
                                                                        self.print_boolean_study(circuit_), line_),
                   r'__image_study__': lambda line_, circuit_: re.sub(r'__image_study__',
                                                                      self.print_img(circuit_, v_range, d_range,
                                                                                     e_range, h_range), line_)
                   }
        for key in methods:
            if re.search(key, line):
                return methods[key](line, circuit)
        return line

    def print_circuit(self, circuit):
        return self.serializer.serialize_circuit_with_attributes(circuit)

    def print_core_attributes(self, circuit, velocity):
        return self.serializer.serialize_core_attributes(circuit, velocity)

    def print_img(self, circuit, v_range, d_range, e_range, h_range):
        return self.serializer.serialize_img_study(circuit, self.study, v_range,
                                                   d_range, e_range, h_range)

    def print_boolean_study(self, circuit):
        return self.serializer.serialize_all_boolean_studies(circuit, self.study)
