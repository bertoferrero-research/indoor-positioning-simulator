import csv

class BufferedCsvFileWriter:
    """
    A class that provides buffered writing functionality to a file.

    Attributes:
        filename (str): The name of the file to write to.
        buffer_size (int): The maximum number of lines to buffer before writing to the file.
        buffer (list): The buffer that holds the lines to be written.

    Methods:
        write(line): Appends a line to the buffer. If the buffer is full, it flushes the buffer to the file.
        flush(): Writes the contents of the buffer to the file.
        close(): Flushes the buffer and closes the file.
    """

    def __init__(self, filename, buffer_size=1000):
        """
        Initializes a new instance of the BufferedCsvFileWriter class.

        Args:
            filename (str): The name of the file to write to.
            buffer_size (int, optional): The maximum number of lines to buffer before writing to the file. Defaults to 1000.
        """
        self.filename = filename
        self.buffer_size = buffer_size
        self.buffer = []

    def write(self, line: list):
        """
        Appends a line to the buffer. If the buffer is full, it flushes the buffer to the file.

        Args:
            line (list): The line to be written to the file.
        """
        self.buffer.append(line)
        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def flush(self):
        """
        Writes the contents of the buffer to the file.
        """
        with open(self.filename, 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.buffer)
        self.buffer = []

    def close(self):
        """
        Flushes the buffer and closes the file.
        """
        if self.buffer:
            self.flush()