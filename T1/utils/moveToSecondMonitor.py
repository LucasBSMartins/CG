from PySide6.QtWidgets import QApplication

class MoveMonitor():
    def center_on_second_monitor(tela):
        """
        Move the window to the center of the second monitor.
        """
        screens = QApplication.screens()  # Get a list of all screens

        if len(screens) > 1:  # Check if there is a second monitor
            second_screen = screens[1]  # Get the second screen
            screen_geometry = second_screen.geometry()  # Get the geometry of the second screen

            # Calculate the center position
            x = screen_geometry.x() + (screen_geometry.width() - tela.width()) - 20
            y = screen_geometry.y() - (screen_geometry.height() - tela.height()) + 500

            # Move the window to the calculated position
            tela.move(x, y)
        else:
            print("No second monitor detected. Window will remain on the primary monitor.")
