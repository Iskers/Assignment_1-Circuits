import pathlib


class PathFinder:
    @staticmethod
    def get_file_path(file_name, folder_name):
        """Returns path to folder_name in package directory for relative file loading"""
        file_path = pathlib.Path(__file__).parent
        return file_path.parent / folder_name / file_name

    @staticmethod
    def get_pure_path(folder_name):
        file_path = pathlib.Path(__file__).parent
        return file_path.parent / folder_name / ""
