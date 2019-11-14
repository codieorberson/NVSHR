import os


class FileManager:
    def __init__(self, file_name, default_lines):
        self._file_name = './dynamic_data/' + file_name
        self._cached_lines = []

        if not os.path.exists(self._file_name):
            with open(self._file_name, "w+") as file:
                file.writelines(default_lines)
            self._cached_lines = default_lines
        else:
            with open(self._file_name) as file:
                self._cached_lines = file.readlines()

    def set_line(self, line_number, line_contents):
        with open(self._file_name, 'r') as file:
            lines = file.readlines()
            lines[line_number] = line_contents
        with open(self._file_name, 'w') as file:
            file.writelines(lines)
        self._cached_lines[line_number] = line_contents

    def append_line(self, line_contents):
        with open(self._file_name, "a") as file:
            file.write(line_contents)
        self._cached_lines.append(line_contents)

    def get_lines(self):
        return self._cached_lines

    def get_line(self, line_number):
        return self._cached_lines[line_number]

    def get_length(self):
        return len(self._cached_lines)
    
    def close(self):
        with open(self._file_name, "w+") as file:
            file.seek(0)
            file.close()
            os.remove(self._file_name)
