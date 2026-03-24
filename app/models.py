from dataclasses import dataclass
from enum import Enum


class SymptomLevel( str,Enum ):
    NONE = "Sín sintomas"
    LIGHT = "Molestias Leves"
    MODERATE = "Visión borrorsa"
    HIGH = "Dolor o visión doble"

@dataclass (slots = True)

class ReviewRecord:
    patient_name: str
    symptom_level: SymptomLevel
    months_since_review: int

    @property
    def urgency_score (self) -> int:
        return calculate_urgency(
            symptom_level = self.symptom_level,
            months_since_review = self.months_since_review
        )
    @property
    def urgency_label (self) ->str:
        score = self.urgency_score
        if score >= 70:
            return "Alta"
        if score >= 40:
            return "Media"
        return  "Baja"


def calculate_urgency (*, symptom_level: SymptomLevel, months_since_review: int) -> int:
        symptom_points = {
            SymptomLevel.NONE: 0,
            SymptomLevel.LIGHT: 20,
            SymptomLevel.MODERATE:45,
            SymptomLevel.HIGH:70,
        }[symptom_level]

        months_points = min(months_since_review * 2 ,30)
        score = symptom_points + months_points
        return min ( score, 100 )