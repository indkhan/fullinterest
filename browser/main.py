import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QAction,
    QLineEdit,
    QProgressBar,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(self.toolbar)

        self.back_btn = QAction("Back", self)
        self.back_btn.triggered.connect(self.browser.back)
        self.toolbar.addAction(self.back_btn)

        self.forward_btn = QAction("Forward", self)
        self.forward_btn.triggered.connect(self.browser.forward)
        self.toolbar.addAction(self.forward_btn)

        self.reload_btn = QAction("Reload", self)
        self.reload_btn.triggered.connect(self.browser.reload)
        self.toolbar.addAction(self.reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


"""1.
First, install Pylnstaller if you havent already:
Copy code
##########pip install pyinstaller
2. Then, navigate to the directory containing your Python script ('browser. py- in
this case) using the command line.
3. Run the following command to create an executable:
Copy code
######pyinstaller --onefile browser.py

4. Pylnstaller will create a *dist- directory containing your executable. You can"""
