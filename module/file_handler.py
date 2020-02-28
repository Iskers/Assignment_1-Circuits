import sys


class File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        try:
            self.open_file = open(self.filename, self.mode)
            return self.open_file
        except OSError:  # pragma: no cover
            sys.stderr.write(f"Could not open file: {self.filename}" + '\n')
            sys.exit()

    def __exit__(self, *args):
        self.open_file.close()
