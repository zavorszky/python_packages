"""
mod_z9hiba.py
Hibakezeléshez általánosan használt dolgok.
"""


# Exception láncolat hibaüzeneteinek összegyűjtése egy sztringbe
# --------------------------------------------------------------
def hibauzenet(p_kivetel: Exception) -> str:
    # huzenet: str = repr(p_kivetel)
    huzenet: str = str(p_kivetel)
    if p_kivetel.__context__ == None:
        return huzenet
    else:
        huzenet = huzenet + " | " + hibauzenet(p_kivetel.__context__)
        return huzenet
