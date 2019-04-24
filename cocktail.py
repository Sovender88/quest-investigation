from flask import Flask, request
import logging
import json
import random
from recipes import cocktail_recipes, child_recipes
from pics import recipes_1, recipes_2


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):

    user_id = req['session']['user_id']

    if req['session']['new']:

        res['response']['text'] = 'Привет! Назови свое имя!'
        sessionStorage[user_id] = {
            'first_name': None,
            'game_started': False
        }

        return

    first_name = get_first_name(req)

    if sessionStorage[user_id]['first_name'] is None:

        if first_name is None:
            res['response']['text'] = 'Не раслышала имя. Повтори!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = 'Приятно познакомиться, ' + first_name.title() + '. Я Алиса. '\
                                                                                       'Хочешь рецепт коктеля?'
            res['response']['buttons'] = [
                {
                    'title': 'Да',
                    'hide': True

                },
                {
                    'title': 'Нет',
                    'hide': True

                },
                {
                    'title': 'Помощь',
                    'hide': True
                }
            ]

    else:

        if not sessionStorage[user_id]['game_started']:

            if 'да' in req['request']['nlu']['tokens']:

                if req['request']['original_utterance'].lower() == 'всё':

                    res['response']['text'] = 'Удачи в приготовлении'
                    res['end_session'] = True

                else:

                    sessionStorage[user_id]['game_started'] = True
                    res['response']['text'] = 'алкогольный или безалкогольный'
                    res['response']['buttons'] = [
                        {
                            'title': 'алкогольный',
                            'hide': True
                        },
                        {
                            'title': 'безалкогольный',
                            'hide': True
                        }
                    ]

                    play_game(res, req)

            elif 'нет' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Ну и ладно!'
                res['end_session'] = True
            elif req['request']['original_utterance'].lower() == 'помощь':
                res['response']['text'] = 'чтобы получить рецепт напишите "ещё";' \
                                          'чтобы закончить, напишите "всё"'
                res['response']['buttons'] = [
                    {
                        'title': 'Да',
                        'hide': True

                    },
                    {
                        'title': 'Нет',
                        'hide': True

                    }
                ]

            elif req['request']['original_utterance'].lower() == 'ещё':
                res['response']['text'] = 'алкогольный или безалкогольный'
                res['response']['buttons'] = [
                    {
                        'title': 'алкогольный',
                        'hide': True
                    },
                    {
                        'title': 'безалкогольный',
                        'hide': True
                    }
                ]

                play_game(res, req)
            else:
                res['response']['text'] = 'Не понял ответа! Так да или нет?'
                res['response']['buttons'] = [
                    {
                        'title': 'Да',
                        'hide': True

                    },
                    {
                        'title': 'Нет',
                        'hide': True

                    },
                    {
                        'title': 'Помощь',
                        'hide': True
                    },
                    {
                        'title': 'ещё',
                        'hide': True
                    },
                    {
                        'title': 'всё',
                        'hide': True
                    },
                    {
                        'title': 'Где попробовать?',
                        'hide': True
                    },
                    {
                        'title': 'алкогольный',
                        'hide': True
                    },
                    {
                        'title': 'безалкогольный',
                        'hide': True
                    }
                ]

        elif req['request']['original_utterance'].lower() == 'помощь':
                res['response']['text'] = 'Это текст помомщи. Будь смелее и продолжи общение.'
        elif req['request']['original_utterance'].lower() == 'алкогольный':
            play_game(res, req)
        elif req['request']['original_utterance'].lower() == 'безалкогольный':
            play_game(res, req)
        elif req['request']['original_utterance'].lower() == 'ещё':
            res['response']['text'] = 'алкогольный или безалкогольный'
            res['response']['buttons'] = [
                {
                    'title': 'алкогольный',
                    'hide': True
                },
                {
                    'title': 'безалкогольный',
                    'hide': True
                }
            ]

            play_game(res, req)
        elif req['request']['original_utterance'].lower() == 'всё':

                    res['response']['text'] = 'Удачи в приготовлении'
                    res['end_session'] = True
        elif req['request']['original_utterance'].lower() == 'Где попробовать?':
            bar(res, req)

'''
тут надо вывести карту с барами москвы
'''
def bar(res, req):
   pass


def play_game(res, req):
    id = '1030494/cba860462f03d20a325a'
    if req['request']['original_utterance'].lower() == 'алкогольный':
        key = random.choice(list(cocktail_recipes.items()))
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Вот и он сам ^-^'
        res['response']['card']['image_id'] = id
        res['response']['text'] = f'''{key[0].lower()}:
                                      {key[1].lower()}'''
    elif req['request']['original_utterance'].lower() == 'безалкогольный':
        key = random.choice(list(child_recipes.items()))
        res['response']['text'] = f'''{key[0].lower()}:
                                      {key[1].lower()}'''
    res['response']['buttons'] = [
        {
            'title': 'Да',
            'hide': True

        },
        {
            'title': 'Нет',
            'hide': True

        },
        {
            'title': 'Помощь',
            'hide': True
        },
        {
            'title': 'ещё',
            'hide': True
        },
        {
            'title': 'всё',
            'hide': True
        },
        {
            'title': 'Где попробовать?',
            'hide': True
        },
        {
            'title': 'алкогольный',
            'hide': True
        },
        {
            'title': 'безалкогольный',
            'hide': True
        }
    ]

    return


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:

        if entity['type'] == 'YANDEX.FIO':

            if 'first_name' in entity['value'].keys():
                return entity['value']['first_name']
            else:
                return None
    return None


if __name__ == '__main__':
    app.run()
