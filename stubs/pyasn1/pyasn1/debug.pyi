import logging
from typing import Any, Literal, TextIO, TypeAlias, TypedDict, type_check_only
from typing_extensions import Unpack

__all__ = ["Debug", "setLogger", "hexdump"]

_DebugFlags: TypeAlias = Literal[0x0000, 0x0001, 0x0002, 0xFFFF]
_FalsyValue: TypeAlias = Literal[0, False] | None

@type_check_only
class _LoggerOptions(TypedDict, total=False):
    loggerName: str | None
    printer: Printer

class Printer:
    def __init__(
        self,
        logger: logging.Logger | None = None,
        handler: logging.StreamHandler[TextIO] | None = None,
        formatter: logging.Formatter | None = None,
    ) -> None: ...
    def __call__(self, msg: Any) -> None: ...  # `msg` is passed to stdlib `logging.debug()`, so can be anything

class Debug:
    defaultPrinter: Printer
    def __init__(self, *flags: Literal["none", "encoder", "decoder", "all"], **options: Unpack[_LoggerOptions]) -> None: ...
    def __call__(self, msg: Any) -> None: ...  # `msg` is passed to `Printer.__call__()`
    def __and__(self, flag: _DebugFlags) -> int: ...
    def __rand__(self, flag: _DebugFlags) -> int: ...

def setLogger(userLogger: Debug | _FalsyValue) -> None: ...  # Falsy values are used to unset
def registerLoggee(module: str, name: str = "LOG", flags: _DebugFlags = 0x0000) -> Debug | Literal[0x0000]: ...
def hexdump(octets: bytes) -> str: ...

class Scope:
    def __init__(self) -> None: ...
    def push(self, token: str) -> None: ...
    def pop(self) -> str: ...
