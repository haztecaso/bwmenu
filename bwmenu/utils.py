from subprocess import Popen, PIPE
import fcntl, os
from typing import List, Tuple

import tldextract


def _set_non_blocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def process_run(cmd:List[str], input=None, **kwargs) -> Tuple[str, str, int]:
    if kwargs.get('verbose', False):
        print(' '.join(cmd))
    process = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
    _set_non_blocking(process.stdout)
    _set_non_blocking(process.stderr)
    stdout, stderr = process.communicate(input=input)
    if process.returncode != 0 and not kwargs.get('ignore_error'):
        raise ProcessError
    return stdout.strip(), stderr.strip(), process.returncode


class ProcessError(Exception):
    pass


def baseurl(url):
    """Get the baseurl (domain+tld) of a url"""
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"


__all__ = ["process_run", "ProcessError", "baseurl"]
