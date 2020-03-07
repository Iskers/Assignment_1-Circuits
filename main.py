import os
import module.parsers as pars
import module.circuit_control as circ
import module.page_generator as pg
import module.path_finder as pf

# Create utility classes
parser = pars.Parser()
page_generator = pg.HTMLPageGenerator()


def default_circuit_function():
    # Define circuit origin file.
    file_name = "task_circuit.tsv"

    # Create circuit class instance
    # The parse function takes in file format and
    circuit = parser.parse(file_name, "tsv", False)

    try:
        circ.CircuitControl.control_circuit(circuit)

    except Exception as fault:
        print(f"Cant use circuit, {fault}")

    else:
        # Generate page with default template and store_location
        page_generator.default_page_generation(circuit)

        while True:
            open_file_query = input("Do you want to open the study?[y / n]")

            if not open_file_query or open_file_query == "y":
                os.system(str(pf.PathFinder.get_file_path("study.html", "templates")))
                break
            elif open_file_query == "n":
                break
            else:
                pass


def circuit_study_with_user_input():
    default_folder_query = input("Default location for circuits is in the data folder. If not, input the location of "
                                 "the circuit file: ")
    file_name = input("Input the name of the circuit file: ")

    accepted_types= ("tsv", "xml")
    if file_name.endswith(accepted_types):
        format_ = file_name.split(".")
        format_ = format_[-1]
    else:
        format_ = input("Input the format of the file: ")

    try:
        if default_folder_query:
            circuit = parser.parse(file_name, format_, default_folder_query)
        else:
            circuit = parser.parse(file_name, format_, False)

    except Exception as fault:
        print(f"Couldn't parse file. {fault}")

    else:
        try:
            circ.CircuitControl.control_circuit(circuit)

        except Exception as fault:
            print(f"Cant use circuit, {fault}")

        else:
            # Generate page with default template and store_location
            template_query = input("Input template file name. Press enter for default: ")
            target_query = input("Input target file name. Press enter for default: ")

            if not template_query and not target_query:
                page_generator.default_page_generation(circuit)

            elif not template_query:
                page_generator.export_circuit_study_in_HTML(circuit, template_query, "study.html")
            elif not target_query:
                page_generator.export_circuit_study_in_HTML(circuit, "study-template.html", target_query)
            else:
                page_generator.export_circuit_study_in_HTML(circuit, template_query, target_query)

            while True:
                open_file_query = input("Do you want to open the study?[y / n] ")
                if not open_file_query or open_file_query == "y":
                    os.system(str(pf.PathFinder.get_file_path("study.html", "templates")))
                    break
                elif open_file_query == "n":
                    break
                else:
                    pass


if __name__ == '__main__':
    #default_circuit_function()
    circuit_study_with_user_input()
