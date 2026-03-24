from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QWidget





class PriorityBar ( QWidget ):

    def __init__(self):
        super().__init__()
        self._value = 0
        self.setMinimumHeight(40)

    def setValue (self, value: int )-> None:
        self._value = max ( 0 , min (100, int (value)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter (self)
        painter.setRenderHint (QPainter.Antialiasing)

        rect = self.rect().adjusted(10, 10, -10, -10)
        painter.setBrush (QColor ("#E5E7EB"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)

        fill_width = rect.width() * self._value / 100
        fill_rect = QRectF (rect.x(), rect.y (),fill_width, rect.height())

        color = QColor ("#22C55E")
        if self._value >=70:
            color = QColor ("#EF4444")
        elif self._value >= 40:
            color = QColor ("#F59E0B")

        painter.setBrush(color)
        painter.drawRoundedRect(fill_rect, 10, 10)

        painter.setPen(QColor("#111827"))
        painter.drawText(rect, Qt.AlignCenter, f"Prioridad: {self._value} / 100")