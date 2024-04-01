from __future__ import annotations

import subprocess
import signal
import sys
import json
import secrets
import socket
import atexit

from types import TracebackType
from typing import Optional, Type, Union, cast

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .base import JupyterConnectable, JupyterConnectionInfo
from .jupyter_client import JupyterClient


class LocalJupyterServer(JupyterConnectable):
    class GenerateToken:
        pass

    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: Optional[int] = None,
        token: Union[str, GenerateToken] = GenerateToken(),
        log_file: str = "jupyter_gateway.log",
        log_level: str = "INFO",
        log_max_bytes: int = 1048576,
        log_backup_count: int = 3,
    ):
        
        if sys.platform == "win32":
            raise ValueError("LocalJupyterServer is not supported on Windows due to kernelgateway bug.")
        
        