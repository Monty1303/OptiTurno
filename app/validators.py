from __future__ import annotations

from typing import Tuple



ValidationResult = Tuple[bool, str]


def validate_patient_name (patient_name: str )-> ValidationResult:
    name = patient_name.strip()

    if len (name) < 3:
        return False , "El nombre debe tener al menos 3 caracteres."

    if any (char.isdigit() for char in name):
        return False, "El nombre no puede contener números."

    return True, ""