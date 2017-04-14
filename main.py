import json
import requests
from PyQt5 import QtWidgets
import sys

api_key = '7d0ef28a2b7e498285a136b363639d31'
sources_url = 'https://newsapi.org/v1/sources'
articles_url = 'https://newsapi.org/v1/articles'
sources_called = False

# Function that pulls articles from the API
def get_articles(source_name):
    names = getsources()[0]
    source_id = names[source_name]
    params = {'source': source_id, 'apiKey': api_key}
    r = requests.get(articles_url, params=params)
    decoded_json = json.loads(r.content)
    list_of_stories = [[article['title'], article['url']]
                       for article in decoded_json['articles']]
    return list_of_stories


# Function that pulls the sources that the API supports
def getsources():
    global sources_called
    default_parems = {'language': 'en'}
    r = requests.get(sources_url, params=default_parems)
    decoded_json = json.loads(r.content)
    list_of_names = [source['name'] for source in decoded_json['sources']]
    if sources_called:
        for item in list_of_names:
            print(item)
        sources_called = False
    list_of_ids = [source['id'] for source in decoded_json['sources']]
    id_name_dictionary = {}
    for a, b in zip(list_of_names, list_of_ids):
        id_name_dictionary[a] = b
    return id_name_dictionary, list_of_names

# Class that defines the elements and functionality of the GUI
class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Function that creates and shows the elements
    def initUI(self):
        title = 'News API Interface'
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.resize(700, 500)

        self.article_txtbox = QtWidgets.QLineEdit()
        self.source_chkbox = QtWidgets.QCheckBox()
        self.submit_btn = QtWidgets.QPushButton('Submit')
        self.output = QtWidgets.QTextEdit()
        self.output.resize(300, 300)

        self.article_label = QtWidgets.QLabel('Source Name:')
        self.source_label = QtWidgets.QLabel('Display Sources?')

        grid.addWidget(self.article_txtbox, 0, 1)
        grid.addWidget(self.source_chkbox, 2, 1)
        grid.addWidget(self.submit_btn, 3, 2)
        grid.addWidget(self.article_label, 0, 0)
        grid.addWidget(self.source_label, 2, 0)
        grid.addWidget(self.output, 0, 2)
        grid.setRowStretch(2, 3)
        self.setWindowTitle(title)

        self.submit_btn.clicked.connect(self.submit)

        self.show()

    # Event that responds to the user clicking the submit button
    def submit(self):
        source = self.article_txtbox.text()
        disp_source = self.source_chkbox.isChecked()
        if disp_source:
            sources = getsources()
            self.print_to_textbx(sources)

        elif source:
            articles = get_articles(source)
            self.print_to_textbx(articles)

    # Function that updates the textbox
    def print_to_textbx(self, text):
        if type(text) == type(tuple()):
            string = ''
            for i in text[1]:
                string += (i + '\n')
            self.output.setText(string)
        else:
            string = ''
            for i in text:
                string += ('Title:' + i[0] + '\n\n' + 'URL:' + i[1] + '\n\n')
            self.output.setText(string)

if __name__ == '__main__':
    root = QtWidgets.QApplication(sys.argv)
    app = App()
    sys.exit(root.exec_())

