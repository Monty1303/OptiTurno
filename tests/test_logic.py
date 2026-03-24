
from OptiTurno.app.models import calculate_urgency, SymptomLevel
from OptiTurno.app.validators import validate_patient_name




def test_calculate_urgency_high():
    score = calculate_urgency(
        symptom_level= SymptomLevel.HIGH,
        months_since_review=15,
    )
    assert score == 100

def test_calculate_urgency_medium():
    score = calculate_urgency(
        symptom_level= SymptomLevel.LIGHT,
        months_since_review=10,
    )
    assert  score == 40

def test_validate_patient_name_invalid ():
    valid, message = validate_patient_name ("Ana2")
    assert  valid is False

def test_validate_patient_name_valid():
    valid, message = validate_patient_name("Ana Lopez")
    assert valid is True
