"""
'mod_log.py' a 'z9log' csomag modulja
* logging_setup(): Naplózás előkészítése
* JSONFormatter_general(): A napló file sorainak json formátumra hozása
Linkek:
Python Exit handlers (atexit): geeksforgeeks: https://www.geeksforgeeks.org/python-exit-handlers-atexit/
"""

import atexit
import logging
import logging.config
import pathlib

import datetime as dt
import pytz
import json
from typing import override

TZ_EUROPE_BUDAPEST = pytz.timezone("Europe/Budapest")

VALID_QUEUE_HANDLER_NAME = "queue_handler"

# Az alábbi kulcsszavak előállítása a:
# lr = logging.LogRecord(....)
# all_attributes = dir(lr)
# print(all_attributes)
LOG_RECORD_BUILTIN_ATTRS = [
    "__class__",
    "__delattr__",
    "__dict__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getstate__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__weakref__",
    "args",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "getMessage",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "taskName",
    "thread",
    "threadName",
]


class Mod_logHiba_konfig_arg_beallitas(Exception):
    def __init__(self, p_logging_config_ffn: str) -> None:
        self.logging_config_ffn = p_logging_config_ffn
        self.queue_handler_name = VALID_QUEUE_HANDLER_NAME
        self.message = f"A 'logging' argumentumainak beolvasása, és/vagy érvényesítése nem sikerült. Konfig file: '{p_logging_config_ffn}', queue handler: {VALID_QUEUE_HANDLER_NAME}."
        super().__init__(self.message)


def logging_setup(p_logging_config_ffn: str) -> None:
    """
    Naplózás előkészítése
    p_logging_config_file:
        json file a logging beállításához.
    p_queue_handler_name:
        A 'p_logging_config_file'-ban megadott handler. Ha helyesen állítjuk be,
        akkor a naplózás nem azonnal történik meg, nem lassítja a program futását
        file műveletekkel, hanem egy queue-ba kerül a napló írása és a program lényegi
        utasításai késedelem nélkül folytatódnak.
    """

    try:
        config_file = pathlib.Path(p_logging_config_ffn)
        with open(config_file) as f:
            config = json.load(f)
        logging.config.dictConfig(config)

        queue_handler = logging.getHandlerByName(VALID_QUEUE_HANDLER_NAME)
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
    except Exception as e:
        raise Mod_logHiba_konfig_arg_beallitas(
            p_logging_config_ffn=p_logging_config_ffn
        ) from e


class JSONFormatter_general(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        # Figyelem!
        # Az 'emsure_ascii' paraméter alapértelmezés szerint 'True',
        # de akkor az ékezetes karakterek nem jelennek meg, csak a kódjuk:
        # pl.: 'ü' helyett a '\u00fc' karakter sorozat.
        # Ha 'False', akkor jó a file-ban is a szöveg.
        return json.dumps(message, ensure_ascii=False, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields: dict = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=TZ_EUROPE_BUDAPEST
            ).isoformat(),
        }

        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message: dict = always_fields
        for key, val in self.fmt_keys.items():
            # key: A message-ben szereplő kulcs.
            # val: Ez a record metódust kell hívni.
            try:
                msg_val = getattr(record, val)
            except Exception:
                msg_val = None

            if msg_val is not None:
                message[key] = msg_val

        for key2, val2 in record.__dict__.items():
            if key2 not in LOG_RECORD_BUILTIN_ATTRS:
                message[key2] = val2

        return message
