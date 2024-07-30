import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QAction,
    QLineEdit,
    QProgressBar,
    QTabWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from googletrans import Translator


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 800, 600)

        self.browser_tabs = QTabWidget()
        self.setCentralWidget(self.browser_tabs)

        self.create_tab("http://www.google.com")

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(self.toolbar)

        self.back_btn = QAction("Back", self)
        self.back_btn.triggered.connect(self.current_browser().back)
        self.toolbar.addAction(self.back_btn)

        self.forward_btn = QAction("Forward", self)
        self.forward_btn.triggered.connect(self.current_browser().forward)
        self.toolbar.addAction(self.forward_btn)

        self.reload_btn = QAction("Reload", self)
        self.reload_btn.triggered.connect(self.current_browser().reload)
        self.toolbar.addAction(self.reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        self.add_translation_option()

    def create_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        self.browser_tabs.addTab(browser, "New Tab")
        browser.urlChanged.connect(self.update_url)

    def current_browser(self):
        return self.browser_tabs.currentWidget()

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def add_translation_option(self):
        translate_action = QAction("Translate", self)
        translate_action.triggered.connect(self.translate_page)
        self.toolbar.addAction(translate_action)

    def translate_page(self):
        translator = Translator()
        current_browser = self.current_browser()
        if current_browser:
            html = current_browser.page().toHtml(self.translate_html)
            translated_text = translator.translate(html, dest="en").text
            current_browser.setHtml(translated_text)

    def translate_html(self, html):
        return html


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
