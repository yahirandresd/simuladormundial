import sys
from PyQt5.QtWidgets import QApplication
from app.views.tournament_view import TournamentView
from app.views.arbol import Arbol
from PyQt5.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icono = QIcon('images/icono.png')
    iconoWindow = QIcon('images/iconowin.png')
    app.setWindowIcon(iconoWindow)
    tournament_view = TournamentView()
    tournament_view.setWindowIcon(icono)
    tournament_view.resize(1920, 800)
    tournament_view.show()

    sys.exit(app.exec_())
