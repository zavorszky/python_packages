from  z9hiba.mod_z9hiba import *
from sys import path

print("** 0 **")
print(path)


print("\n** 1 **")
hiba = NincsHiba(p_prg_nev="prgnev_1")
print(hiba)
print("prg_nev=", hiba.prg_nev)
print("hiba_kod=", hiba.hiba_kod)
print("hiba_uzenet=", hiba.hiba_uzenet)
print("getOsszetettHibauzenet", hiba.getOsszetettHibauzenet())

print("\n** 2 **")
hiba2a = EgyebHiba(
    p_prg_nev="prgnev_2",
    p_hiba_uzenet="Egyéb 'a' hiba",
    p_hiba_kivetel=Exception("Komoly hiba"),
)

hibak2 = Hibak()
hibak2.addHiba(p_hiba=hiba)
hibak2.addHiba(p_hiba=hiba2a)
print(hibak2)
print(hibak2.hibak)
print(hibak2.getUtolsoHiba())
print(hibak2.getUtolsoHiba().getOsszetettHibauzenet())
