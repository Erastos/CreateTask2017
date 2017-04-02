import argparse
import requests


def initiate_cmd():
    desciption = \
                'Takes in strings and outputs the language and the confidence'
    parser = argparse.ArgumentParser(description=desciption)
    parser.add_argument('-a', help='Outputs the top stories from input source')
    parser.add_argument('-s', help='Outputs the source used by News API')
    arguments = vars(parser.parse_args())
    mode_manager(arguments)


def getArticles(source_name):
    print('reached articles')


def getsources():
    print('reached sources')


def mode_manager(arguments):
    for argument in arguments.items():
        for index, key in enumerate(argument):
            if key == 'a':
                getArticles(argument[index + 1])
            elif key == 's':
                getsources()


initiate_cmd()
