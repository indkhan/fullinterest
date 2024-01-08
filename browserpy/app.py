import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QAction, QComboBox, QHBoxLayout, QScrollArea
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from googletrans import Translator


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Browser')
        self.translator = Translator()
        self.language = 'en'  # Default language: English

        self.browser = QWebEngineView()
        # Set Google as the default URL in English
        self.browser.setUrl(QUrl('https://www.google.com/?hl=en'))
        self.browser.titleChanged.connect(self.update_title)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.load_finished)

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

        self.back_button = QPushButton('Back')
        self.back_button.setToolTip('Go back to the previous page')
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton('Forward')
        self.forward_button.setToolTip('Go forward to the next page')
        self.forward_button.clicked.connect(self.browser.forward)

        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignCenter)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.url_label)
        input_layout.addWidget(self.url_bar)
        input_layout.addWidget(self.search_button)
        input_layout.addWidget(self.clear_button)
        input_layout.addWidget(self.reload_button)
        input_layout.addWidget(self.back_button)
        input_layout.addWidget(self.forward_button)

        translate_scroll = QScrollArea()
        translate_scroll.setWidgetResizable(True)
        translate_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        translate_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        translate_layout = QVBoxLayout()
        translate_layout.addWidget(self.translate_button)
        translate_layout.addWidget(QLabel('Translate to:'))

        self.language_selector = QComboBox()
        # Add more languages as needed
        self.language_selector.addItems(['English', 'Spanish', 'French'])
        self.language_selector.setCurrentText(
            'English')  # Default language selector
        self.language_selector.currentIndexChanged.connect(
            self.change_language)
        translate_layout.addWidget(self.language_selector)
        translate_layout.addStretch(1)

        translate_container = QWidget()
        translate_container.setLayout(translate_layout)
        translate_scroll.setWidget(translate_container)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addWidget(translate_scroll)
        layout.addWidget(self.browser)
        layout.addWidget(self.status_bar)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.statusBar().showMessage('Ready')

        self.create_menu()

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

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
        translated_page = self.translator.translate(
            self.browser.page().toHtml(), src='auto', dest='en')
        self.browser.setHtml(translated_page.text)
        self.browser.setUrl(QUrl(current_url))

    def change_language(self):
        language_mapping = {'English': 'en', 'Spanish': 'es',
                            'French': 'fr'}  # Add more languages if needed
        selected_language = self.language_selector.currentText()
        self.language = language_mapping[selected_language]

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f'Simple Browser - {title}')

    def update_progress(self, progress):
        self.status_bar.setText(f'Loading... {progress}%')

    def load_finished(self):
        self.status_bar.setText('Loaded')

    def clear_input(self):
        self.url_bar.clear()

    def reload_page(self):
        self.browser.reload()


def main():
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
