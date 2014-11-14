"""
Core utility classes for mpzip.
"""

import os
import subprocess

class ProcessStream(object):
    """
    A file-like object for decompressing data from a process.  Closing the stream will also wait
    for process termination.
    """

    def __init__(self, name, proc, stream, check):
        """
        Construct a new process stream.  This will generally be done by one of the compression type
        wrappers.

        :param name: The name of the compression/decompession program.
        :param proc: The process object.
        :param fd: The file descriptor.
        :param mode: The file mode.
        :param check: Whether to check the process results.
        :return:
        """
        super(ProcessStream, self).__init__()
        self.name = name
        self._process = proc
        self._file = stream
        self.check_proc = check

    def close(self):
        """
        Close the file descriptor and the process.
        :return: Nothing
        """

        try:
            self._file.close()
        finally:
            rc = self._process.wait()
            if self.check_proc and rc != 0:
                raise IOError('%s failed with code %d' % (self.name, rc))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.close()
        else:
            try:
                self.close()
            except:
                pass

            return False

    def __iter__(self):
        return self

    def next(self):
        return self._file.next()

    def __getattr__(self, item):
        return getattr(self._file, item)

def open_decompressor(cmd, fn=None, check=False):
    """
    Open a decompression stream.
    :param cmd: The command, as a list of arguments.
    :param fn: The file name (or ``None`` if the file name is included in the arguments).
    :param check: Whether to check the result of the command when closing the stream.
    :return: A decompression stream (file-like object).
    """

    if fn is None:
        stdin = None
    else:
        stdin = os.open(fn, os.O_RDONLY)

    proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, close_fds=True)
    if stdin is not None:
        os.close(stdin)
    return ProcessStream(cmd[0], proc, proc.stdout, check)

def open_compressor(cmd, fn=None, append=False):
    """
    Open a decompression stream.
    :param cmd: The command, as a list of arguments.
    :param fn: The file name (or ``None`` if the file name is included in the arguments).
    :return: A decompression stream (file-like object).
    """

    if fn is None:
        stdout = None
    else:
        flags = os.O_WRONLY | os.O_CREAT
        if append:
            flags |= os.O_APPEND
        else:
            flags |= os.O_TRUNC
        stdout = os.open(fn, flags)

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, close_fds=True)
    if stdout is not None:
        os.close(stdout)
    return ProcessStream(cmd[0], proc, proc.stdin, True)
