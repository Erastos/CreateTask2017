import argparse
import requests
import json
import pdb

api_key = '7d0ef28a2b7e498285a136b363639d31'
sources_url = 'https://newsapi.org/v1/sources'
articles_url = 'https://newsapi.org/v1/articles'
sources_called = False


def initiate_cmd():
    desciption = \
                'Takes in strings and outputs the language and the confidence'
    parser = argparse.ArgumentParser(description=desciption)
    parser.add_argument('-a', help='Outputs the top stories from input source')
    parser.add_argument('-s', help='Outputs the source used by News API',
                        action='store_true')
    arguments = vars(parser.parse_args())
    mode_manager(arguments)


def getArticles(source_name):
    names = getsources()
    source_id = names[source_name]
    parems = {'source': source_id, 'apiKey': api_key}
    r = requests.get(articles_url, params=parems)
    decoded_json = json.loads(r.content)
    list_of_stories = [[article['title'], article['url']]
                       for article in decoded_json['articles']]
    for i in list_of_stories:
        print("Title: %s\n Url: %s\n\n\n" % (i[0], i[1]))


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
    return id_name_dictionary


def mode_manager(arguments):
    for argument in arguments.items():
        for index, key in enumerate(argument):
            if key == 'a':
                if argument[index + 1] is not None:
                    getArticles(argument[index + 1])
            elif key == 's':
                if argument[index + 1]:
                    global sources_called
                    sources_called = True
                    getsources()


initiate_cmd()
