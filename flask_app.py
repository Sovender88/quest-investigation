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
                },
                {
                    'title': 'Действующие лица',
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
                    play_game(res, req)



            elif 'нет' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Ну и ладно!'
                res['end_session'] = True
            elif req['request']['original_utterance'].lower() == 'действующие лица':
                characters(res)
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
                    'title': 'Действующие лица',
                    'hide': True
                    }
            ]
            elif req['request']['original_utterance'].lower() == 'помощь':
                help(res)
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
                    'title': 'Действующие лица',
                    'hide': True
                    }
            ]
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
                    'title': 'Действующие лица',
                    'hide': True
                    }
            ]
        elif req['request']['original_utterance'].lower() == 'помощь':
                help(res)

        else:
            play_game(res, req)


def play_game(res, req):
    a = 0
   
    text(res, a)
    res['response']['buttons'] = [
        {
            'title': 'Продолжить',
            'hide': True
            }
        ]
    a += 1
    if req['request']['original_utterance'].lower() == 'продолжить':
        text(res, a)
        res['response']['buttons'] = [
        {
            'title': 'Далее',
            'hide': True
            }
        ]
    a += 1
    if req['request']['original_utterance'].lower() == 'далее':
        text(res, a)
        res['response']['buttons'] = [
        {
            'title': 'Наведу справки о группе студентов Киттинг',
            'hide': True
            },
        {
            'title': 'Перечитаю материалы дела Стэнгард',
            'hide': True
            },
        {
            'title': 'Пойду в бар и напьюсь',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'наведу справки о группе студентов киттинг':
        information(res, req)
    if req['request']['original_utterance'].lower() == 'далее':
        pass
    if req['request']['original_utterance'].lower() == 'далее':
        pass
    return

def text(res, a):
    ans_list = [''' 
                    Вы – Нэйт Лэхи, офицер полиции. Обладаете незаурядным умом и можете раскрыть даже самое запутанное дело.
                    Пропала Лайла Стэнгард, студентка. О её пропаже заявила одна из её подруг. В последний раз девушку видели 30 августа 2014 года на вечеринке в Университете Миддлтон,
                    на которой она застукала своего парня, Гриффина О’Райли и подругу Ребекку Саттер вместе, разозлилась и ушла. После этого её никто не видел.
                ''',
                '''
                    Несколько дней спустя, её тело было найдено в резервуаре на крыше кампуса. О’Райли и Саттер были арестованы на следующий после этого день.
                    Известно, что Ребекка работала в баре за пределами кампуса, где студенты покупали наркотики. Она привлекалась за хранение и продажу.
                ''',
                '''
                    Сейчас 7 часов вечера. Ваш рабочий день окончен, но вы сидите в пустом офисе, потому что вас не покидает одно смутное подозрение по поводу нераскрытого дела. Итак, что же вы будете делать?
                '''

    ]
    res['response']['text'] = ans_list[a]
    return
def information_text(res, a):
    ans_list = [''' 
                    Каждый год Аннализ Киттинг берёт к себе в помощники наиболее способных студентов со своего курса.
                    Они борются за приз: статуэтку Фемиды с завязанными глазами, который получит студент, проявивший себя наилучшим образом. ''',
                '''
                    Вы порылись в базе данных и вот что там нашли: мать Уэса Гиббинса иммигрировала из Гаити в Соединённые Штаты и начала работать в семье Махони.
                    Она покончила с собой, когда ему было 12. Про отца ничего не известно.
                ''',
                ''' 
                    Родители Лорел Кастильо разведены, живут в Испании. Отец может быть замешан в чём-то противозаконном. В 16 лет она была похищена, выкуп за неё не был заплачен.
                ''',
                ''' 
                    У Микаэллы Пратт отличное резюме и идеальная характеристика. Её отец застрелил её мать, когда ей было 2 года.
                ''',
                '''
                    Вы читали досье очередного студента, как вдруг у вас зазвонил телефон. 
                ''',
                '''
                    Звонит Аннализ Киттинг. Вы расстались после того, как на последнем заседании она вызвала вас в качестве свидетеля и заставила признаться в том,
                    что в вашем отделе были случаи фальсификации улик. Вы на неё злитесь, но понимаете, что она может звонить по делу. Возьмёте трубку или сбросите? 
                '''
    ]
    res['response']['text'] = ans_list[a]
    return

def information(res, req):
    a = 0
    res['response']['buttons'] = [
        {
            'title': 'дальше',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'дальше':
        information_text(res, a)
    a += 1
    return


def help(res):
    res['response']['text'] = '''
    Данная игра представляет собой текстовый квест. Вам будет предложено сыграть за детектива Нэйла Лэхи, которому предстоит расследовать убийство. Вам будут предложены несколько вариантов ответа, благодоря которым вы будите продвигаться по сюжету и раскроете убийство. Приятной игры'''


def characters(res):
    res['response']['text'] = '''
    • Аннализ Киттинг – адвокат, преподаёт в Университете Миддлтон право,жена Сэма Киттинга, имеет свою частную фирму.
    • Сэм Киттинг – психолог, муж Аннализ, преподаёт в Университете Миддлтон философию.
    • Нэйт Лэхи – детектив, бывший любовник Аннализ.
    • Уэс Гиббинс – студент Аннализ.
    • Коннор Уолш – студент Аннализ.
    • Микаэлла Пратт – студентка Аннализ.
    • Ашер Миллстоун – студент Аннализ.
    • Лорел Кастильо – студентка Аннализ.
    • Фрэнк Дельфино – сотрудник фирмы Аннализ.
    • Бонни Уинтерботтом – сотрудница фирмы Аннализ.
    • Оливер Хэмптон – парень Коннора, IT-специалист.
    • Лайла Стэнгард – бывшая любовница Сэма, его студентка.'''


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
