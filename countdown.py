import sys
import os
import math
from datetime import datetime, date
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush, QFontDatabase, QPainter, QPen
from PySide6.QtCore import Qt, QTimer, QUrl, QPointF
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class AnalogClock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.time = datetime.now()

        # Timer for updating the clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Shadow effect for a refined look
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)

    def update_time(self):
        self.time = datetime.now()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Clock dimensions
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 10

        # Clock face (gradient)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#FFF0F5"))  # Lavender blush
        gradient.setColorAt(1, QColor("#E6E6FA"))  # Lavender
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor("#483D8B"), 2))  # Dark slate blue
        painter.drawEllipse(center, radius, radius)

        # Hour markers
        painter.setPen(QPen(QColor("#6A5ACD"), 2))  # Slate blue
        for i in range(12):
            angle = i * 30  # 360 / 12
            rad = math.radians(angle)
            outer = radius * 0.9
            inner = radius * 0.8
            painter.drawLine(
                center + QPointF(outer * math.sin(rad), -outer * math.cos(rad)),
                center + QPointF(inner * math.sin(rad), -inner * math.cos(rad))
            )

        # Minute markers
        for i in range(60):
            if i % 5 != 0:  # Skip hour markers
                angle = i * 6  # 360 / 60
                rad = math.radians(angle)
                outer = radius * 0.9
                inner = radius * 0.85
                painter.setPen(QPen(QColor("#6A5ACD"), 1))
                painter.drawLine(
                    center + QPointF(outer * math.sin(rad), -outer * math.cos(rad)),
                    center + QPointF(inner * math.sin(rad), -inner * math.cos(rad))
                )

        # Hour hand
        hour_angle = (self.time.hour % 12 + self.time.minute / 60) * 30
        hour_rad = math.radians(hour_angle)
        hour_length = radius * 0.5
        painter.setPen(QPen(QColor("#483D8B"), 4))
        painter.drawLine(
            center,
            center + QPointF(hour_length * math.sin(hour_rad), -hour_length * math.cos(hour_rad))
        )

        # Minute hand
        minute_angle = (self.time.minute + self.time.second / 60) * 6
        minute_rad = math.radians(minute_angle)
        minute_length = radius * 0.7
        painter.setPen(QPen(QColor("#6A5ACD"), 3))
        painter.drawLine(
            center,
            center + QPointF(minute_length * math.sin(minute_rad), -minute_length * math.cos(minute_rad))
        )

        # Second hand
        second_angle = self.time.second * 6
        second_rad = math.radians(second_angle)
        second_length = radius * 0.8
        painter.setPen(QPen(QColor("#FF6F61"), 2))  # Coral for contrast
        painter.drawLine(
            center,
            center + QPointF(second_length * math.sin(second_rad), -second_length * math.cos(second_rad))
        )

        # Center dot
        painter.setBrush(QBrush(QColor("#483D8B")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, 5, 5)

        painter.end()

class CountdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clock & Countdown to July 10, 2025")
        self.setGeometry(100, 100, 600, 600)  # Increased height for analog clock

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Gradient background
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0, QColor("#FFE4E1"))  # Pastel pink
        gradient.setColorAt(1, QColor("#ADD8E6"))  # Light blue
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#6A5ACD"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#D8BFD8"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#6A5ACD"))
        self.setPalette(palette)

        # Font
        font = QFont("Roboto", 20)  # Slightly smaller for balance
        font.setWeight(QFont.Weight.Bold)
        small_font = QFont("Roboto", 14)

        # Analog clock
        self.analog_clock = AnalogClock()
        layout.addWidget(self.analog_clock, alignment=Qt.AlignmentFlag.AlignCenter)

        # Digital clock label
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setFont(font)
        self.clock_label.setStyleSheet("""
            color: #6A5ACD;
            background-color: #D8BFD8;
            border-radius: 8px;
            padding: 12px;
        """)
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        self.clock_label.setGraphicsEffect(shadow)
        layout.addWidget(self.clock_label)

        # Countdown title
        countdown_title = QLabel("Countdown to July 10, 2025")
        countdown_title.setFont(small_font)
        countdown_title.setStyleSheet("color: #483D8B;")
        countdown_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shadow_title = QGraphicsDropShadowEffect()
        shadow_title.setBlurRadius(10)
        shadow_title.setColor(QColor(0, 0, 0, 80))
        shadow_title.setOffset(2, 2)
        countdown_title.setGraphicsEffect(shadow_title)
        layout.addWidget(countdown_title)

        # Countdown label
        self.countdown_label = QLabel("0 hours, 0 minutes, 0 seconds")
        self.countdown_label.setFont(font)
        self.countdown_label.setStyleSheet("""
            color: #6A5ACD;
            background-color: #D8BFD8;
            border-radius: 8px;
            padding: 12px;
        """)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shadow_countdown = QGraphicsDropShadowEffect()
        shadow_countdown.setBlurRadius(15)
        shadow_countdown.setColor(QColor(0, 0, 0, 80))
        shadow_countdown.setOffset(2, 2)
        self.countdown_label.setGraphicsEffect(shadow_countdown)
        layout.addWidget(self.countdown_label)

        # Stretch to balance layout
        layout.addStretch()

        # Music setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(script_dir, "Prateek Kuhad - Co2 (Official Audio) 4.wav")
        if os.path.exists(audio_path):
            print(f"Audio file found at: {audio_path}")
            audio_url = QUrl.fromLocalFile(audio_path)
            self.player.setSource(audio_url)
            self.player.play()
            self.player.errorOccurred.connect(self.handle_media_error)
        else:
            print(f"Audio file not found at: {audio_path}")
            print("Please place 'Prateek Kuhad - Co2 (Official Audio) 4.wav' in the same directory as the script.")

        # Timers
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

        # Initial updates
        self.update_clock()
        self.update_countdown()

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.setText(current_time)

    def update_countdown(self):
        target_date = datetime(2025, 7, 10, 0, 0, 0)
        current_date = datetime.now()
        delta = target_date - current_date

        if delta.total_seconds() <= 0:
            self.countdown_label.setText("The moment has arrived!")
            self.countdown_timer.stop()
            return

        total_hours = int(delta.total_seconds() // 3600)
        minutes = (int(delta.total_seconds()) % 3600) // 60
        seconds = int(delta.total_seconds()) % 60

        self.countdown_label.setText(f"{total_hours} hours, {minutes} minutes, {seconds} seconds")

    def handle_media_error(self, error):
        print(f"Media Player Error: {self.player.errorString()} (Error code: {error})")

    def closeEvent(self, event):
        print("Application closing, stopping audio")
        self.player.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#6A5ACD"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#D8BFD8"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#6A5ACD"))
    app.setPalette(palette)

    # Try to set Roboto font
    font_db = QFontDatabase()
    if "Roboto" not in font_db.families():
        print("Roboto font not found, falling back to sans-serif")
        app.setFont(QFont("SansSerif", 10))

    window = CountdownApp()
    window.show()
    sys.exit(app.exec())
