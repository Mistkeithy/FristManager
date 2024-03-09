import os
import datetime

class Logger:
    instance = None

    def __init__(self, verbose=2, debug=False, file_path=None):
        """
        comment me in english
        """
        self.verbose = verbose
        self.debug = debug
        self.file_path = file_path if file_path else os.path.join(os.getcwd(), "bot.log")
        self.log_entry = ""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                pass

    @classmethod
    def getInstance(cls, verbose=2, debug=False, file_path=None):
        """
        comment me in english
        """
        if cls.instance is None:
            cls.instance = Logger(verbose, debug, file_path)
        return cls.instance

    def drop_logging(self, status, level):
        """
        comment me in english
        """
        if level > self.verbose or (status == 5 and not self.debug):
            return True
        return False

    def get_status_name(self, status):
        """
        comment me in english
        """
        status_string = "INFO"
        status_map = {
            1: "WARNING",
            2: "ERROR",
            3: "FATAL",
            4: "ACCESS",
            5: "DEBUG",
            6: "SUCCESS"
        }
        return status_map.get(status, status_string)

    def get_time_stamp(self):
        """
        comment me in english
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_log_entry(self, log_entry, status, level, log_header=True):
        """
        comment me in english
        """
        header = f"{level} [{self.get_status_name(status)}] {self.get_time_stamp()} - " if log_header else ""
        self.log_entry = f"{header}{log_entry}"

    def get_log_entry(self):
        """
        comment me in english
        """
        return self.log_entry

    def write_console(self, input_text, status=1, level=3, log_header=True):
        """
        comment me in english
        """
        print(self.get_log_entry())

    def write_file(self, input_text, status=1, level=3, log_header=True):
        """
        comment me in english
        """
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(self.get_log_entry() + "\n")

    def write(self, input_text, status=1, level=3, log_on_console=True, log_to_file=True, log_header=True):
        """
        comment me in english
        """
        if self.drop_logging(status, level):
            return
        self.set_log_entry(input_text, status, level, log_header)

        if log_on_console:
            self.write_console(input_text, status, level, log_header)
        if log_to_file:
            self.write_file(input_text, status, level, log_header)