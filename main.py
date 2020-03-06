import module.file_handler as fh
import module.path_finder as pf
import module.parsers as pars
import module.circuit as cir

if __name__ == '__main__':
    # Define circuit origin file.
    file_name = "task_circuit.tsv"

    # Create utility classes
    parser = pars.Parser()

    # Create circuit class instance
    # The parse function takes in file format and
    circuit = parser.parse(file_name, "tsv", False)


    cir.Circuit

    file_name = "task_circuit.tsv"
    parser = pars.Parser()
    circuit = parser.parse(file_name, "tsv", False)
    print(circuit.efficiency)
    circuit.efficiency = 0.5
    print(circuit.efficiency)
    print(circuit.canvas)
