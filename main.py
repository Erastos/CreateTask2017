# Module used for decoding json
import json

# Module used for interacting with API
import requests

# Modules used for GUI implementation
from PyQt5 import QtWidgets
import sys

# API Key used for the News API
api_key = '7d0ef28a2b7e498285a136b363639d31'
# URL used for pulling the sources that News API
sources_url = 'https://newsapi.org/v1/sources'
# URL used for pulling down the articles tied to a certain source
articles_url = 'https://newsapi.org/v1/articles'
# Boolean Flag that checks to see if the user called the getsources function
sources_called = False


def get_articles(source_name):
    # Gets a dictionary containing the sources and their ids
    names = getsources()[0]
    # Loads the specific source id that the user passes to the program
    source_id = names[source_name]
    # Creates the parameters that will be passed to the api
    params = {'source': source_id, 'apiKey': api_key}
    # Gets the api's response with the parameters created above
    r = requests.get(articles_url, params=params)
    # Decodes the JSON response of the api
    decoded_json = json.loads(r.content)
    # Pulls the title and the url from the response
    list_of_stories = [[article['title'], article['url']]
                       for article in decoded_json['articles']]
    # Prints the title and the url to the screen
    return list_of_stories


# Function that pulls the sources that the API supports
def getsources():
    # Gets the sources_called variable called eariler
    global sources_called
    # Tells the API to only return english sources
    default_parems = {'language': 'en'}
    # Gets the API's response
    r = requests.get(sources_url, params=default_parems)
    # Decodes the JSON response
    decoded_json = json.loads(r.content)
    # Pulls the names of the sources from the decoded JSON
    list_of_names = [source['name'] for source in decoded_json['sources']]
    # If the user asks to see the sources, print out each source that the API
    # returned
    if sources_called:
        for item in list_of_names:
            print(item)
        sources_called = False
    # Gather all of the source ids into a list
    list_of_ids = [source['id'] for source in decoded_json['sources']]
    # Create an empty dicitonary
    id_name_dictionary = {}
    # Loop through the source names and ids and put them in a dictionary
    for a, b in zip(list_of_names, list_of_ids):
        id_name_dictionary[a] = b
    # Return the dictionary
    return id_name_dictionary, list_of_names


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

    def submit(self):
        source = self.article_txtbox.text()
        disp_source = self.source_chkbox.isChecked()
        if disp_source:
            sources = getsources()
            self.print_to_textbx(sources)

        elif source:
            articles = get_articles(source)
            self.print_to_textbx(articles)

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


root = QtWidgets.QApplication(sys.argv)
app = App()
sys.exit(root.exec_())
