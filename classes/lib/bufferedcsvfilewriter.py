# Copyright 2024 Alberto Ferrero López
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    def __init__(self, filename, buffer_size=1000, enabled=True):
        """
        Initializes a new instance of the BufferedCsvFileWriter class.

        Args:
            filename (str): The name of the file to write to.
            buffer_size (int, optional): The maximum number of lines to buffer before writing to the file. Defaults to 1000.
            enabled (bool, optional): Specifies whether the BufferedCsvFileWriter is enabled or not. Defaults to True.
        """
        self._filename = filename
        self._buffer_size = buffer_size
        self._buffer = []
        self.enabled = enabled

    @property
    def filename(self):
        return self._filename

    def write(self, line: list):
        """
        Appends a line to the buffer. If the buffer is full, it flushes the buffer to the file.

        Args:
            line (list): The line to be written to the file.
        """
        if not self.enabled:
            return
        self._buffer.append(line)
        if len(self._buffer) >= self._buffer_size:
            self.flush()

    def flush(self):
        """
        Writes the contents of the buffer to the file.
        """
        if not self._buffer:
            return
        with open(self._filename, 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self._buffer)
        self._buffer = []

    def close(self):
        """
        Flushes the buffer and closes the file.
        """
        if self._buffer:
            self.flush()