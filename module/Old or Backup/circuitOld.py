from package.module.parts import *

'''
def canvasResizeLength(canvas: list, length: int = 1):
    canvas.append([None] * len(canvas[0]))
    if length < 0:
        for i in reversed(range(len(canvas) - 1)):
            canvas[i + 1] = canvas[i]
        canvas[0] = [None] * len(canvas[0])
    return canvas


# Increases the canvas height
def canvasResizeHeight(canvas: list, height: int = 1):
    for i in canvas:
        i.append(None)
    if height < 0:
        for i in range(len(canvas)):
            for j in reversed(range(len(canvas[i]) - 1)):
                canvas[i][j + 1] = canvas[i][j]
        for i in canvas:
            i[0] = None
        return canvas
    else:
        return canvas
'''


class Circuit:
    canvas: list = [[None, None],[None, None]]

    def __init__(self):
        self.current_position = [0, 0]

    def canvas_creator(self):
        user_input = 0
        final_tank = False
        self.canvas = []

        while user_input != 999:
            user_input = input("Please give a input: ")
            user_input = int(user_input)

            if user_input == 000:
                self.canvas = []

            elif user_input == 1:
                tank_name = input("Give the tank a name: ")
                if not final_tank:
                    self.canvas.append([Tank(tank_name)])
                else:
                    pass

    def __str__(self):
        return str(self.canvas)

    def canvas_placer(self, part: Part):
        user_input = input("Where do you want to put %s? " % part)
        user_input = user_input.lower()  # TODO: check lower
        if user_input == "u":
            try:
                if self.canvas[self.current_position[0]][self.current_position[1] - 1] is None:
                    self.canvas[self.current_position[0]][self.current_position[1] - 1] = part
                else:
                    raise Exception["Invalid input! Space already occupied. Try another direction"]

            except IndexError:
                self.canvas_resize_height(-1)
                self.canvas[self.current_position[0]][self.current_position[1] - 1] = part  # TODO Test this shit
            finally:
                self.current_position[1] = self.current_position[1] - 1

        elif user_input == "d":
            try:
                if self.canvas[self.current_position[0]][self.current_position[1] + 1] is None:
                    self.canvas[self.current_position[0]][self.current_position[1] + 1] = part
                else:
                    raise Exception["Invalid input! Space already occupied. Try another direction"]
            except IndexError:
                self.canvas_resize_height(1)
                self.canvas[self.current_position[0]][self.current_position[1] + 1] = part  # TODO Test this shit
            finally:
                self.current_position[1] = self.current_position[1] + 1

        elif user_input == "l":
            try:
                if self.canvas[self.current_position[0] - 1][self.current_position[1]] is None:
                    self.canvas[self.current_position[0] - 1][self.current_position[1]] = part
                else:
                    raise Exception["Invalid input! Space already occupied. Try another direction"]
            except IndexError:
                self.canvas_resize_length(-1)
                self.canvas[self.current_position[0] - 1][self.current_position[1]] = part  # TODO Test this shit
            finally:
                self.current_position[0] = self.current_position[0] - 1

        elif user_input == "r":
            try:
                if self.canvas[self.current_position[0] + 1][self.current_position[1]] is None:
                    self.canvas[self.current_position[0] + 1][self.current_position[1]] = part
                else:
                    raise Exception["Invalid input! Space already occupied. Try another direction"]
            except IndexError:
                self.canvas_resize_length(1)
                self.canvas[self.current_position[0] + 1][self.current_position[1]] = part  # TODO Test this shit
            finally:
                self.current_position[0] = self.current_position[0] + 1
        else:
            raise ValueError("Invalid input! Expected chars, u,d,r,l. You typed: {}".format(user_input))

    # Increases the canvas length
    def canvas_resize_length(self, length: int = 1):
        self.canvas.append([None] * len(self.canvas[0]))
        if length < 0:
            for i in reversed(range(len(self.canvas) - 1)):
                self.canvas[i + 1] = self.canvas[i]
            self.canvas[0] = [None] * len(self.canvas[0])
        return self.canvas

    # Increases the canvas height
    def canvas_resize_height(self, height: int = 1):
        for i in self.canvas:
            i.append(None)
        if height < 0:
            for i in range(len(self.canvas)):
                for j in reversed(range(len(self.canvas[i]) - 1)):
                    self.canvas[i][j + 1] = self.canvas[i][j]
            for i in self.canvas:
                i[0] = None
            return self.canvas
        else:
            return self.canvas
