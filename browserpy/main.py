import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QAction, QComboBox, QHBoxLayout, QScrollArea, QTabWidget, QShortcut
from PyQt5.QtCore import QUrl, Qt, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from googletrans import Translator


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Browser')
        self.translator = Translator()
        self.language = 'en'  # Default language: English
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.create_new_tab()

        self.browser = self.tabs.currentWidget()
        self.browser.titleChanged.connect(self.update_title)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.load_finished)
        self.browser.installEventFilter(self)

        self.url_label = QLabel('Enter URL or search:')
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('Type a URL or search term')
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.search_button = QPushButton('Search')
        self.search_button.setToolTip('Search the web for the entered query')
        self.search_button.clicked.connect(self.search_query)

        self.translate_button = QPushButton('Translate')
        self.translate_button.setToolTip(
            'Translate the current page to English')
        self.translate_button.clicked.connect(self.translate_page)

        self.clear_button = QPushButton('Clear')
        self.clear_button.setToolTip('Clear the URL/Search bar')
        self.clear_button.clicked.connect(self.clear_input)

        self.reload_button = QPushButton('Reload')
        self.reload_button.setToolTip('Reload the current page')
        self.reload_button.clicked.connect(self.reload_page)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.url_label)
        input_layout.addWidget(self.url_bar)
        input_layout.addWidget(self.search_button)
        input_layout.addWidget(self.clear_button)
        input_layout.addWidget(self.reload_button)
        input_layout.addWidget(self.translate_button)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.statusBar().showMessage('Ready')

        self.create_menu()
        self.create_shortcuts()

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')

        new_tab_action = QAction('New Tab', self)
        new_tab_action.setShortcut(Qt.CTRL + Qt.Key_T)
        new_tab_action.triggered.connect(self.create_new_tab)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut(Qt.CTRL + Qt.Key_Q)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_tab_action)
        file_menu.addAction(exit_action)

    def create_shortcuts(self):
        new_tab_shortcut = QShortcut(Qt.CTRL + Qt.Key_T, self)
        new_tab_shortcut.activated.connect(self.create_new_tab)

    def create_new_tab(self):
        new_browser = QWebEngineView()
        new_browser.setUrl(QUrl('https://www.google.com/?hl=en'))
        new_browser.titleChanged.connect(self.update_title)
        new_browser.loadProgress.connect(self.update_progress)
        new_browser.loadFinished.connect(self.load_finished)
        self.tabs.addTab(new_browser, 'New Tab')

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'https://' + url
        self.browser.setUrl(QUrl(url))

    def search_query(self):
        query = self.url_bar.text()
        search_url = f"https://www.google.com/search?q={query}"
        self.browser.setUrl(QUrl(search_url))

    def translate_page(self):
        current_url = self.browser.url().toString()
        self.browser.page().toHtml(self.translated_content)

    def translated_content(self, translated_html):
        translated_page = self.translator.translate(
            translated_html, src='auto', dest='en')
        self.browser.setHtml(translated_page.text)

    def update_title(self):
        index = self.tabs.currentIndex()
        current_browser = self.tabs.widget(index)
        title = current_browser.page().title()
        self.tabs.setTabText(index, title)
        self.setWindowTitle(f'Simple Browser - {title}')

    def update_progress(self, progress):
        self.statusBar().showMessage(f'Loading... {progress}%')

    def load_finished(self):
        self.statusBar().showMessage('Loaded')

    def clear_input(self):
        self.url_bar.clear()

    def reload_page(self):
        self.browser.reload()

    def eventFilter(self, obj, event):
        if obj == self.browser:
            if event.type() == QEvent.KeyPress:
                key = event.key()
                modifiers = event.modifiers()
                if modifiers == Qt.ControlModifier:
                    if key == Qt.Key_R:
                        self.reload_page()
                    elif key == Qt.Key_W:
                        self.close_tab(self.tabs.currentIndex())
        return super().eventFilter(obj, event)


def main():
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
