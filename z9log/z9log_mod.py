# Projekt: n/a
# Rövid leírás: Program napló, log file írás támogatása.
# File: z9log_mod.py
# Programkód tipus: Python module
# Feladat:
#   Logoláshoz logger szolgáltatása.
#   Ha meg van a "z9log.cfg" konfigurációs file, akkor annak a beállítása szerint
#   történik a loggolás, ha nincs meg, akkor a program beállít néhány jellemzőt.
# Felhasználás:
#   import z9log_mod
#   log = z9log_mod.get_logger(p_logger_name=__name__, p_logfile_name="z9log_test.log")
# Info:
#   * python: Logging HOWTO: https://docs.python.org/3/howto/logging.html#logging-howto
#   * python: logging — Logging facility for Python: https://docs.python.org/3/library/logging.html
#   * stackoverflow: Python logging: use milliseconds in time format: https://stackoverflow.com/questions/6290739/python-logging-use-milliseconds-in-time-format
#     A "z9log.cfg"-ben a log rekord formátumának beállításához hasznos.
# Készült: 2024-05-11
# Szerző: zavorszky@yahoo.com

import os
import logging
import logging.config
import z9hiba.mod_z9hiba

# Konstansok
# ----------
LOGCFGFILE_NAME = "z9log.cfg"
LOGCFGFILE_ENCODING = "utf-8"
LOGFILE_ENCODING = "utf-8"

LOG_LINEFORMAT = "%(asctime)s [%(levelname)s] %(message)s"


# Függvények
# ----------
def get_logger(p_logger_name, p_logfile_name, p_hibak):
    try:
        logger = logging.getLogger(p_logger_name)
        if os.path.exists(LOGCFGFILE_NAME):
            """
            Van a logozást beállító konfigurációs file.
            """
            logging.config.fileConfig(
                LOGCFGFILE_NAME,
                defaults={"logfilename": p_logfile_name},
                disable_existing_loggers=False,
                encoding=LOGCFGFILE_ENCODING,
            )
        else:
            """
            A logozás jellemzőit a program állítja be.
            """
            logging.basicConfig(
                filename=p_logfile_name,
                format=LOG_LINEFORMAT,
                encoding=LOGFILE_ENCODING,
                level=logging.DEBUG,
            )
        p_hibak.addHiba(z9hiba.mod_z9hiba.NincsHiba(p_prg_nev="get_logger"))
        return logger
    except Exception as e:
        p_hibak.addHiba(
            z9hiba.mod_z9hiba.EgyebHiba(
                p_prg_nev="get_logger",
                p_hiba_uzenet="Nem sikerült a loggert beállítani.",
                p_hiba_kivetel=e,
            )
        )
        return None
