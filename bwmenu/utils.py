from subprocess import Popen, PIPE, CalledProcessError
from typing import List, Tuple
import fcntl, os


def _set_non_blocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def process_run(cmd:List[str], input=None) -> Tuple[str, str]:
    process = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
    _set_non_blocking(process.stdout)
    _set_non_blocking(process.stderr)
    result = process.communicate(input=input)
    if process.returncode != 0:
        raise ProcessError
    return result[0].strip(), result[0].strip()


class ProcessError(Exception):
    pass

__all__ = ["process_run", "ProcessError"]
