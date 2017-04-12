# Module implements the command line interface
import argparse
# Module used for interacting with API
import requests
# Module used for decoding json
import json

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QCheckBox, QGridLayout, QLabel, QTextEdit
import sys

# API Key used for the News API
api_key = '7d0ef28a2b7e498285a136b363639d31'
# URL used for pulling the sources that News API
sources_url = 'https://newsapi.org/v1/sources'
# URL used for pulling down the articles tied to a certain source
articles_url = 'https://newsapi.org/v1/articles'
# Boolean Flag that checks to see if the user called the getsources function
sources_called = False


# Function initiates and creates the command line interface
def initiate_cmd():
    # Description for the command line program
    description = \
        'Takes in strings and outputs the language and the confidence'
    parser = argparse.ArgumentParser(description=description)
    # -a is the argument that outputs articles
    parser.add_argument('-a', help='Outputs the top stories from input source')
    # -s is the argument that outputs the sources
    parser.add_argument('-s', help='Outputs the source used by News API',
                        action='store_true')
    # imports arguments that the user passes to the program
    arguments = vars(parser.parse_args())
    # Calls the flag management function
    mode_manager(arguments)


def get_articles(source_name):
    # Gets a dictionary containing the sources and their ids
    names = getsources()
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
    for i in list_of_stories:
        print("Title: %s\n Url: %s\n\n\n" % (i[0], i[1]))


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
    return id_name_dictionary


# Function that handles the control flow of the program
def mode_manager(arguments):
    for argument in arguments.items():
        # Checks to see if the key is a or s, and then calls the right function
        for index, key in enumerate(argument):
            if key == 'a':
                if argument[index + 1] is not None:
                    get_articles(argument[index + 1])
            elif key == 's':
                if argument[index + 1]:
                    global sources_called
                    sources_called = True
                    getsources()


# Starts the command line interface
# initiate_cmd()


class app(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = 'News API Interface'
        grid = QGridLayout()
        self.setLayout(grid)

        article_txtbox = QLineEdit()
        source_chkbox = QCheckBox()
        submit_btn = QPushButton('Submit')
        output = QTextEdit()

        article_label = QLabel('Source Name:')
        source_label = QLabel('Display Sources?')

        grid.addWidget(article_txtbox, 0, 1)
        grid.addWidget(source_chkbox, 2, 1)
        grid.addWidget(submit_btn, 3, 2)
        grid.addWidget(article_label, 0, 0)
        grid.addWidget(source_label, 2, 0)
        grid.addWidget(output, 0, 2)
        self.setWindowTitle(title)
        self.show()


root = QApplication(sys.argv)
app = app()
sys.exit(root.exec_())
