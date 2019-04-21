from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

get_sack = False
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
            res['response']['text'] = 'Приятно познакомиться, ' + first_name.title()
            res['response']['text'] = 'Сыграем?'
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

                if get_sack:

                    res['response']['text'] = 'вас уволилил'
                    res['end_session'] = True

                else:

                    sessionStorage[user_id]['game_started'] = True
                    
                   

            elif 'нет' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Ну и ладно!'
                res['end_session'] = True
            elif req['request']['original_utterance'].lower() == 'помощь':
                res['response']['text'] = 'помоги расслед'
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
                    }
                ]
        elif req['request']['original_utterance'].lower() == 'помощь':
                res['response']['text'] = 'Это текст помомщи. Будь смелее и продолжи общение.'









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