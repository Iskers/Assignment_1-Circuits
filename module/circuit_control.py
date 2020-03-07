import module.circuit as cir
import module.parts as pt


class CircuitControl:
    def __init__(self):
        pass

    @staticmethod
    def control_circuit(circuit: cir.Circuit):
        """
        Takes in a circuit and returns either an exception or the value True.

        :param circuit:
        :return: Validness of circuit
        """
        tank_count_check = 0
        pump_count_check = 0
        current_angle_check = 0
        inside_diameter_check = None
        previous_part = None
        valve_check_part = None

        if not isinstance(circuit[0], pt.Tank) or not isinstance(circuit[-1], pt.Tank):
            raise Exception(f"{circuit[0]}, first or last part is not a Tank, first is {circuit[0]}, "
                            f"last is {circuit[-1]}.")

        for part in circuit.canvas:

            # Control number of Tanks
            if isinstance(part, pt.Tank):
                tank_count_check += 1
                if tank_count_check > 2:
                    raise Exception(f"{part!r}, too many pumps, there must not be more than two tanks.")

            # Control that the part before the previous valve has the correct angle
            if valve_check_part is not None:
                if not isinstance(part, pt.Pipe):
                    raise Exception(f"{part!r}, part before and after {previous_part} must be a pipe and is not.")

                elif isinstance(part, pt.PipeStraight):
                    if part.angle != current_angle_check:
                        raise Exception(f"{part!r}, part before and after {previous_part} must be pipes with the same "
                                        f"angle. Part before is {valve_check_part}.")
                valve_check_part = None

            # Control that a tank is followed by a horizontal pipe
            if isinstance(previous_part, pt.Tank):
                if isinstance(part, pt.PipeStraight):
                    if part.angle == 0:
                        pass
                else:
                    raise Exception(f"{part!r}, {previous_part} must be followed by a horizontal pipe and is not.")

            # Control Pumps and Filters
            elif isinstance(part, pt.Pump) or isinstance(part, pt.Filter):
                if not isinstance(previous_part, pt.PipeStraight):
                    raise Exception(f"{part!r}, {previous_part} should be a pipe and is not.")
                elif previous_part.angle != 0:
                    raise Exception(f"{part!r}, type pump and filter should be preceded by a horizontal pipe and is not.")

            # Control Valves
            elif isinstance(part, pt.Valve):
                if valve_check_part is None:
                    if not isinstance(previous_part, pt.Pipe):
                        raise Exception(f"{part!r}, {previous_part} preceding type Valve is not a pipe")
                    valve_check_part = previous_part

            # Control that a pipe has the correct diameter and that a pipe is followed by the right angle pipe.
            elif isinstance(part, pt.Pipe):
                if inside_diameter_check is None:
                    inside_diameter_check = part.inside_diameter
                else:
                    if part.inside_diameter != inside_diameter_check:
                        raise Exception(f"{part!r}, all pipes in circuit must have the same inside diameter. Inside "
                                        f"diameter set for this circuit is {inside_diameter_check}.")

                if isinstance(previous_part, pt.PipeStraight) and isinstance(part, pt.PipeStraight):
                    if part.angle != previous_part.angle:
                        raise Exception(f"{part!r}, pipes following each other must have the same angle,"
                                        f" previous part {previous_part}.")

            # Control pump count, should not be more than 1
            if isinstance(part, pt.Pump):
                pump_count_check += 1
                if pump_count_check > 1:
                    raise Exception(f"{part!r}, too many pumps, there must not be more than one pump.")

            # Control bends
            if isinstance(part, pt.PipeBend):
                if current_angle_check == 0:
                    current_angle_check = 90
                else:
                    current_angle_check = 0

                if not isinstance(previous_part, pt.PipeStraight) or isinstance(previous_part, pt.Valve):
                    raise Exception(f"{part!r}, bends should be preceded by either pipes or valves.")

            # Control that pipes, pumps, filters against angles
            if isinstance(part, pt.PipeStraight):
                # Control pumps and filters
                if isinstance(previous_part, pt.Pump) or isinstance(previous_part, pt.Filter):
                    if part.angle != 0:
                        raise Exception(f"{part!r}, pumps and filters should be followed by a horizontal pipe.")

                # Control angle of pipes
                elif isinstance(previous_part, pt.PipeBend) or isinstance(part, pt.PipeStraight):
                    if part.angle != current_angle_check:
                        raise Exception(f"{part!r}, This pipe has an angle of {part.angle}"
                                        f" while the angle should be {current_angle_check}.")

            previous_part = part
        return True
