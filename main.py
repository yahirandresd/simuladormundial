import sys
from PyQt5.QtWidgets import QApplication
from app.views.tournament_view import TournamentView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tournament_view = TournamentView()
    tournament_view.resize(1000, 800)
    tournament_view.show()
    sys.exit(app.exec_())