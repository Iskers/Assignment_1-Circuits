import module.parsers as pars

if __name__ == '__main__':
    file_name = "task_circuit.tsv"
    parser = pars.Parser()
    circuit = parser.parse(file_name, "tsv", False)
    print(circuit.efficiency)
    circuit.efficiency = 0.5
    print(circuit.efficiency)
    print(circuit.canvas)