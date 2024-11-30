"""
mod_konfig.py
Konfiguráció file (adatbázis/registry) kezelő modul.
"""

__version__ = "2.0"

__all__ = [
    "KonfigHiba_a_konfig_file_nem_letezik",
    "KonfigHiba_a_konfig_file_olvasasa_sikertelen",
    "KonfigHiba_a_konfig_ft_hibas",
    "KonfigRegDBKezelo",
]

__author__ = "zavorszky@yahoo.com"

import os
import configparser


# A mod_konfig modul hiba osztályai
# ---------------------------------
class KonfigHiba_a_konfig_file_nem_letezik(FileNotFoundError):
    def __init__(self, p_ffn: str) -> None:
        self.ffn = p_ffn
        self.message = f"Hiba:A '{p_ffn}' konfig file nem létezik."
        super().__init__(self.message)


class KonfigHiba_a_konfig_file_olvasasa_sikertelen(OSError):
    def __init__(self, p_ffn: str) -> None:
        self.ffn = p_ffn
        self.message = f"Hiba:A '{p_ffn}' konfig file beolvasása nem sikerült."
        super().__init__(self.message)


class KonfigHiba_a_konfig_ft_hibas(ValueError):
    def __init__(self, p_ffn: str, p_ft_valodi: str, p_ft_ervenyes: str) -> None:
        self.ffn = p_ffn
        self.ft_hvalodi = p_ft_valodi
        self.ft_ervenyes = p_ft_ervenyes
        self.message = f"Hiba:A '{p_ffn}' konfig file tipusa '{p_ft_valodi}' hibás. A helyes: '{p_ft_ervenyes}'."
        super().__init__(self.message)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class KonfigRegDBKezelo:
    # ffn : Konfiguráció Full File Name
    # ft: Konfiguráció File Type
    # cp: Config Parser
    def __init__(self, p_ffn: str, p_ft_ervenyes: str):
        self.ffn = p_ffn
        self.ft_ervenyes = p_ft_ervenyes
        self.ft_valodi = None
        self.cp = None

        if not os.path.exists(self.ffn):
            raise KonfigHiba_a_konfig_file_nem_letezik(self.ffn)

        self.cp = configparser.ConfigParser()
        try:
            self.cp.read(self.ffn)
        except Exception as e:
            raise KonfigHiba_a_konfig_file_olvasasa_sikertelen(self.ffn) from e

        self.ft_valodi: str = self.cp.get("alap", "ft")
        if not self.ft_valodi == self.ft_ervenyes:
            raise KonfigHiba_a_konfig_ft_hibas(
                self.ffn, self.ft_valodi, self.ft_ervenyes
            )
