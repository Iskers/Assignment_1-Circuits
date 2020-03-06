import pathlib


class PathFinder:
    file_path = pathlib.Path(__file__).parent

    @classmethod
    def get_folder_path(cls, folder_name):
        return cls.file_path.parent / folder_name / ""

    @classmethod
    def get_file_path(cls, file_name, folder_name):
        """Returns path to folder_name in package directory for relative file loading"""
        return cls.file_path.parent / folder_name / file_name
