from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, \
    QComboBox, QSpinBox, QLabel, QPushButton, QTableWidget, QMessageBox, QTableWidgetItem

from  OptiTurno.app.models  import ReviewRecord, SymptomLevel, calculate_urgency
from  OptiTurno.app.validators import validate_patient_name
from  OptiTurno.app.widgets import PriorityBar


class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle( "OptiTurno")

        self.resize (820,500)
        self.records: list[ReviewRecord] =  []

        self._build_ui()
        self._connect_signals()
        self._update_preview()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout ()

        layout.addLayout(left_layout,2)
        layout.addLayout(right_layout,3)

        form_box = QGroupBox ("Nueva Revisión")
        form_layout = QFormLayout (form_box)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText ("Nombre del paciente ")

        self.symptom_input = QComboBox ()
        for level in SymptomLevel:
            self.symptom_input.addItem(level.value, level)

        self.months_input = QSpinBox()
        self.months_input.setRange(0, 60)
        self.months_input.setValue(12)
        self.months_input.setSuffix("meses")

        form_layout.addRow("Paciente: ", self.name_input)
        form_layout.addRow("Sintomas: ", self.symptom_input)
        form_layout.addRow("Última revisión: ", self.months_input)

        left_layout.addWidget(form_box)

        preview_box = QGroupBox("Vista previa")
        preview_layout = QVBoxLayout(preview_box)

        self.priority_bar = PriorityBar()
        self.preview_label = QLabel ()
        self.preview_label.setAlignment(Qt.AlignCenter)

        preview_layout.addWidget(self.priority_bar)
        preview_layout.addWidget(self.preview_label)

        left_layout.addWidget(preview_box)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton ("Añadir")
        self.clear_button = QPushButton ("limpiar")

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.clear_button)

        left_layout.addLayout(buttons_layout)
        left_layout.addStretch()

        table_box = QGroupBox("Listado de revisiones")
        table_layout = QVBoxLayout(table_box)

        self.table = QTableWidget (0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Paciente", "Sintomas","Meses","Prioridad"]
        )
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        table_layout.addWidget(self.table)

        self.info_label = QLabel ("Todavia no hay revisiones registradas.")
        self.info_label.setWordWrap(True)
        table_layout.addWidget(self.info_label)

        right_layout.addWidget(table_box)

    def _connect_signals (self):
        self.name_input.textChanged.connect(self._update_preview)
        self.symptom_input.currentIndexChanged.connect(self._update_preview)
        self.months_input.valueChanged.connect(self._update_preview)

        self.add_button.clicked.connect(self._add_record)
        self.clear_button.clicked.connect(self._clear_form)

    def _current_symptom_level (self) -> SymptomLevel:
        data = self.symptom_input.currentData()
        if isinstance(data,SymptomLevel):
            return data
        return SymptomLevel (data)

    def _update_preview (self):
        score = calculate_urgency (
            symptom_level = self._current_symptom_level(),
            months_since_review = self.months_input.value()

        )
        self.priority_bar.setValue(score)

        if score >= 70 :
            label = "Alta"
        elif score >= 40:
            label = "Media"
        else:
            label = "Baja"

        self.preview_label.setText(f"Prioridad estimdada: {label}")

    def _add_record(self) -> None:
        is_valid, message = validate_patient_name(self.name_input.text())

        if not is_valid:
            QMessageBox.warning (self, "Validación", message)
            return

        record =  ReviewRecord(
            patient_name = self.name_input.text().strip(),
            symptom_level= self._current_symptom_level(),
            months_since_review = self.months_input.value()
        )

        self.records.append(record)
        self._refresh_table()
        self._clear_form()

    def _clear_form (self):
        self.name_input.clear()
        self.symptom_input.setCurrentIndex(0)
        self.months_input.setValue(12)
        self._update_preview()

    def _refresh_table(self) -> None:
        sorted_records = sorted(self.records, key=lambda r: r.urgency_score, reverse=True)

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(sorted_records))

        for row, record in enumerate(sorted_records):
            symptom_text = (
                record.symptom_level.value
                if hasattr(record.symptom_level, "value")
                else str(record.symptom_level)
            )

            values = [
                record.patient_name,
                symptom_text,
                str(record.months_since_review),
                f"{record.urgency_label} ({record.urgency_score})",
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)

                if column == 3:
                    if record.urgency_score >= 70:
                        item.setBackground(QColor("#FCA5A5"))
                    elif record.urgency_score >= 40:
                        item.setBackground(QColor("#FDE68A"))
                    else:
                        item.setBackground(QColor("#BBF7D0"))

                self.table.setItem(row, column, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

        if self.records:
            urgent = max(self.records, key=lambda r: r.urgency_score)
            self.info_label.setText(
                f"Revisión con mayor prioridad: {urgent.patient_name} "
                f"({urgent.urgency_label}, {urgent.urgency_score}/100)."
            )
        else:
            self.info_label.setText("Todavía no hay revisiones registradas.")
