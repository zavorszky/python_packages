# Projekt: n/a
# Rövid leírás: Naplózás tesztelése.
# File: z9log_test.py
# Programkód tipus: Python test
# Feladat: ...
# Felhasználás:
#   > & python z9log_test.py
# Info:
#   ...
# Készült: 2024-05-11
# Szerző: zavorszky@yahoo.com

from z9log.z9log_mod import get_logger
from z9hiba.mod_z9hiba import Hibak


hibak = Hibak()
log = get_logger(p_logger_name=__name__, p_logfile_name="./test/z9log_test.log", p_hibak=hibak)
log.info("1.Indul logozás teszt...")
log.info("2.logozás...")
log.info("3.Vége a logozás tesztnek.")
