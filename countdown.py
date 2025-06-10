import sys
import os
from datetime import datetime, date
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush, QFontDatabase
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class CountdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clock & Countdown to July 10, 2025")
        self.setGeometry(100, 100, 600, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Font
        font = QFont("Roboto", 24)
        font.setWeight(QFont.Weight.Bold)
        small_font = QFont("Roboto", 16)

        # Color palette
        self.setStyleSheet("background-color: #FFE4E1;")  # Pastel pink

        # Clock label
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setFont(font)
        self.clock_label.setStyleSheet("color: #6A5ACD; padding: 10px;")  # Slate blue
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clock_label)

        # Countdown title
        countdown_title = QLabel("Countdown to July 10, 2025")
        countdown_title.setFont(small_font)
        countdown_title.setStyleSheet("color: #483D8B;")  # Dark slate blue
        countdown_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(countdown_title)

        # Countdown label
        self.countdown_label = QLabel("0 hours, 0 minutes, 0 seconds")
        self.countdown_label.setFont(font)
        self.countdown_label.setStyleSheet("""
            color: #6A5ACD;
            background-color: #D8BFD8;
            border-radius: 10px;
            padding: 15px;
        """)  # Pastel purple
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.countdown_label)

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
    palette.setColor(QPalette.ColorRole.Window, QColor("#FFE4E1"))
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
