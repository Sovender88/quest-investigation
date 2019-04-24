from flask import Flask, request
import logging
import json

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
            res['response']['text'] = 'Приятно познакомиться, ' + first_name.title() + '. Сыграем?'
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
                res['response']['text'] = 'Это текст помомщи. Будь смелее и продолжи общение.'

        else:
            if req['request']['original_utterance'].lower() == 'начать сначала' or req['request']['original_utterance'].lower() == 'да' or req['request']['original_utterance'].lower() == 'продолжить' or req['request']['original_utterance'].lower() == 'далее' or req['request']['original_utterance'].lower() == 'наведу справки о группе студентов киттинг' or req['request']['original_utterance'].lower() == 'перечитаю материалы дела стэнгард' or req['request']['original_utterance'].lower() == 'пойду в бар и напьюсь':
                play_game(res, req)

            elif req['request']['original_utterance'].lower() == 'узнать про лорел и микаэллу'or req['request']['original_utterance'].lower() == 'посмотреть на телефон' or req['request']['original_utterance'].lower() == 'проигнорировать':
                spravki(res, req)

            elif req['request']['original_utterance'].lower() == 'узнать кто звонит' or req['request']['original_utterance'].lower() == 'не обращать внимания':
                materials(res, req)

            elif req['request']['original_utterance'].lower() == 'ответить' or req['request']['original_utterance'].lower() == 'сбросить' or req['request']['original_utterance'].lower() == 'помочь аннализ' or req['request']['original_utterance'].lower() == 'дальше' or req['request']['original_utterance'].lower() == 'спустя сутки':
                phone(res, req)

            elif req['request']['original_utterance'].lower() == 'следующий день':
                bar(res, req)

            elif req['request']['original_utterance'].lower() == 'допросить' or req['request']['original_utterance'].lower() == 'не допрашивать' or req['request']['original_utterance'].lower() == 'независимое расследование':
                prison(res, req)

            elif req['request']['original_utterance'].lower() == 'обыскать машину сэма' or req['request']['original_utterance'].lower() == 'достать запись допроса реббеки' or req['request']['original_utterance'].lower() == 'поехать в офис' or req['request']['original_utterance'].lower() == 'продолжить незвасимое расследование':
                rassled(res, req)

            elif req['request']['original_utterance'].lower() == 'поехать на рабочее место' or req['request']['original_utterance'].lower() == 'не проводить допрос' or req['request']['original_utterance'].lower() == 'провести допрос':
                prison2(res, req)

            elif req['request']['original_utterance'].lower() == 'продолжить расследование' or req['request']['original_utterance'].lower() == 'спустя несколько часов':
                rassled2(res, req)

            elif req['request']['original_utterance'].lower() == 'пригласить сэма в качестве психолога' or req['request']['original_utterance'].lower() == 'допросить сэма' or req['request']['original_utterance'].lower() == 'перекусить' or req['request']['original_utterance'].lower() == 'поехать и перекусить':
                next(res, req)

            elif req['request']['original_utterance'].lower() == 'вызову на допрос гриффина о’райли' or req['request']['original_utterance'].lower() == 'попробую выяснить, где сейчас ребекка':
                part2(res, req)

            elif req['request']['original_utterance'].lower() == 'отправиться в суд':
                pobeg1(res, req)

            elif req['request']['original_utterance'].lower() == 'поехать в суд':
                pobeg2(res, req)

            elif req['request']['original_utterance'].lower() == 'попробовать выяснить, где сейчас ребекка' or req['request']['original_utterance'].lower() == 'вызовать на допрос гриффина о’райли' or req['request']['original_utterance'].lower() == 'отправиться домой спать':
                part1(res, req)

            elif req['request']['original_utterance'].lower() == 'ждать' or req['request']['original_utterance'].lower() == 'найду улики, чтобы дискредитировать кигана и его эксперта' or req['request']['original_utterance'].lower() == 'передам материалы аннализ' or req['request']['original_utterance'].lower() == 'постараюсь убедить родителей лайлы запретить эксгумацию её тела' or req['request']['original_utterance'].lower() == 'узнаю, кто слил информацию в прессу':
                sud(res, req)

            elif req['request']['original_utterance'].lower() == 'продолжать заседание' or req['request']['original_utterance'].lower() == '-->' or req['request']['original_utterance'].lower() == 'посмотреть сериал, по мативам которого была создана игра':
                best_end(res, req)


def play_game(res, req):
    res['response']['text'] = '''
        Вы – Нэйт Лэхи, офицер полиции. Обладаете незаурядным умом и можете раскрыть даже самое запутанное дело.
        Пропала Лайла Стэнгард, студентка. О её пропаже заявила одна из её подруг. В последний раз девушку видели 30 августа 2014 года на вечеринке в Университете Миддлтон, на которой она застукала своего парня, Гриффина О’Райли и подругу Ребекку Саттер вместе, разозлилась и ушла. После этого её никто не видел.'''
    res['response']['buttons'] = [
        {
            'title': 'Продолжить',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'продолжить':
        res['response']['text'] = '''
            Несколько дней спустя, её тело было найдено в резервуаре на крыше кампуса. О’Райли и Саттер были арестованы на следующий после этого день.
            Известно, что Ребекка работала в баре за пределами кампуса, где студенты покупали наркотики. Она привлекалась за хранение и продажу.'''
        res['response']['buttons'] = [
        {
            'title': 'Далее',
            'hide': True
            }
        ]
    elif req['request']['original_utterance'].lower() == 'далее':
        res['response']['text'] = '''
            Сейчас 7 часов вечера. Ваш рабочий день окончен, но вы сидите в пустом офисе, потому что вас не покидает одно смутное подозрение по поводу нераскрытого дела. Итак, что же вы будете делать?'''
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
    elif req['request']['original_utterance'].lower() == 'наведу справки о группе студентов киттинг':
        spravki(res, req)
    elif req['request']['original_utterance'].lower() == 'перечитаю материалы дела стэнгард':
        materials(res, req)
    elif req['request']['original_utterance'].lower() == 'пойду в бар и напьюсь':
        bar(res, req)
    return


def spravki(res, req):
    res['response']['text'] = '''
        Каждый год Аннализ Киттинг берёт к себе в помощники наиболее способных студентов со своего курса. Они борются за приз: статуэтку Фемиды с завязанными глазами, который получит студент, проявивший себя наилучшим образом.
        Вы порылись в базе данных и вот что там нашли: мать Уэса Гиббинса иммигрировала из Гаити в Соединённые Штаты и начала работать в семье Махони. Она покончила с собой, когда ему было 12. Про отца ничего не известно.'''
    res['response']['buttons'] = [
        {
            'title': 'Узнать про Лорел и Микаэллу',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'узнать про лорел и микаэллу':
        res['response']['text'] = '''
            Родители Лорел Кастильо разведены, живут в Испании. Отец может быть замешан в чём-то противозаконном. В 16 лет она была похищена, выкуп за неё не был заплачен.
            У Микаэллы Пратт отличное резюме и идеальная характеристика. Её отец застрелил её мать, когда ей было 2 года.
            Вы читали досье очередного студента, как вдруг у вас зазвонил телефон.'''
        res['response']['buttons'] = [
        {
            'title': 'Посмотреть на телефон',
            'hide': True
            },
        {
            'title': 'Проигнорировать',
            'hide': True
            }
        ]
    elif req['request']['original_utterance'].lower() == 'посмотреть на телефон':
        phone(res, req)
    elif req['request']['original_utterance'].lower() == 'проигнорировать':
        bar(res, req)
    return


def materials(res, req):
    res['response']['text'] = '''
        Вы решили освежили в памяти материалы дела, но не нашли ничего нового и поехали домой.
        Сели в машину, как вдруг у вас зазвонил телефон.'''
    res['response']['buttons'] = [
        {
            'title': 'Узнать кто звонит',
            'hide': True
            },
        {
            'title': 'Не обращать внимания',
            'hide': True}
        ]
    if req['request']['original_utterance'].lower() == 'узнать кто звонит':
        phone(res, req)
    elif req['request']['original_utterance'].lower() == 'не обращать внимания':
        bar(res, req)
    return


def phone(res, req):
    res['response']['text'] = '''
        Звонит Аннализ Киттинг. Вы расстались после того, как на последнем заседании она вызвала вас в качестве свидетеля и заставила признаться в том, что в вашем отделе были случаи фальсификации улик. Вы на неё злитесь, но понимаете, что она может звонить по делу. Возьмёте трубку или сбросите?'''
    res['response']['buttons'] = [
        {
            'title': 'Ответить',
            'hide': True
            },
        {
            'title': 'Сбросить',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'ответить':
        res['response']['text'] = '''
            Аннализ говорит, что она подозревает Сэма в причастности к убийству Лайлы и просит вас ей помочь, а именно: выяснить, где был её муж в ночь с 29 на 30 августа. Её голос дрожит, даже по телефону понятно, что она очень переживает, и вы, переборов злость, соглашаетесь ей помочь.'''
        res['response']['buttons'] = [
            {
                'title': 'Помочь Аннализ',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'помочь аннализ':
        res['response']['text'] = '''
            Вы решили разобраться с этим как можно быстрее, и на следующий же день поехали в Коннектикут.
            Сэм должен был читать лекцию по философии в Йельском университете, но он там не появился, в последний момент сказав, что он отравился. Декан университета был в ярости: он хотел переманить профессора Киттинга к себе, но после этого инцидента передумал.'''
        res['response']['buttons'] = [
            {
                'title': 'Дальше',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'дальше':
        res['response']['text'] = '''
            После университета вы поехали в отель, где останавливался Сэм, и выяснили, что его машина была на парковке каждую ночь, кроме одной: с 29 на 30 августа. Он уехал в семь вечера, а вернулся на следующий день в шесть утра.
            Теперь уже и у вас начинают появляться подозрения по поводу причастности Сэма.'''
        res['response']['buttons'] = [
            {
                'title': 'Спустя сутки',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'спустя сутки':
        prison(res, req)

    elif req['request']['original_utterance'].lower() == 'сбросить':
        bar(res, req)
    return


def prison(res, req):
    res['response']['text'] = '''
        События развиваются стремительно: вы только что узнали, что Аннализ Киттинг взялась защищать Ребекку Саттер, но последняя призналась в убийстве Лайлы. Её признание зафиксировано на видео, но видео не приобщено к материалам дела.
        Это кажется вам подозрительным, вы начинаете думать, что Ребекку призналась в убийстве подруги под давлением.
        Хотите сами её допросить?'''
    res['response']['buttons'] = [
        {
            'title': 'Допросить',
            'hide': True
            },
        {
            'title': 'Не допрашивать',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'допросить':
        res['response']['text'] = '''
            Ребекка призналась вам, что она никого не убивала, и что её заставили признаться в убийстве, потому что Гриффин О’Райли уже всё рассказал, и по его версии, виновата Ребекка. '''
        res ['response']['buttons'] = [
            {
                'title': 'Независимое расследование',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'не допрашивать':
        res['response']['text'] = '''
            Вы решили не допрашивать Ребекку, а вместо этого пойти перекусить.'''
        res ['response']['buttons'] = [
            {
                'title': 'Независимое расследование',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'независимое расследование':
        rassled(res, req)
    return


def rassled(res, req):
    res['response']['text'] = '''
        Вы не стали говорить Аннализ, что не уверены в невиновности её мужа, чтобы лишний раз её не тревожить, а сами начали независимое расследование. Итак, что вы сделаете первым делом?'''
    res['response']['buttons'] = [
        {
            'title': 'Обыскать машину Сэма',
            'hide': True
            },
        {
            'title': 'Достать запись допроса Реббеки',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'обыскать машину сэма':
        res['response']['text'] = '''
            Вы порылись в телефоне Сэма, который он оставил в машине, и выяснили, что в ночь убийства Лайлы Стэнгард он был в городе.
            За несанкционированным обыском вас застукала Бонни Уинтерботтом, наблюдавшая из своей машины.'''
        res['response']['buttons'] = [
            {
                'title': 'Поехать в офис',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'поехать в офис':
        first_end(res, req)
    elif req['request']['original_utterance'].lower() == 'достать запись допроса реббеки':
        res['response']['text'] = '''
            Пришлось включить смекалку и немного надавить на офицера, у которого была видеозапись, но вы её заполучили.
            На записи ясно видно, что показания Ребекка давала под давлением со стороны следователя.
            Вы передали запись Бонни Уинтерботтом.'''
        res['response']['buttons'] = [
            {
                'title': 'Продолжить незвасимое расследование',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'продолжить незвасимое расследование':
        next(res, req)
    return


def prison2(res, req):
    res['response']['text'] = '''
        События развиваются стремительно: вы только что узнали, что Аннализ Киттинг взялась защищать Ребекку Саттер, но последняя призналась в убийстве Лайлы. Её признание зафиксировано на видео, но видео не приобщено к материалам дела.
        Это кажется вам подозрительным, вы начинаете думать, что Ребекку призналась в убийстве подруги под давлением.
        Хотите сами её допросить?'''
    res['response']['buttons'] = [
        {
            'title': 'Провести допрос',
            'hide': True
            },
        {
            'title': 'Не проводить допрос',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'провести допрос':
        res['response']['text'] = '''
            Ребекка призналась вам, что она никого не убивала, и что её заставили признаться в убийстве, потому что Гриффин О’Райли уже всё рассказал, и по его версии, виновата Ребекка. '''
        res ['response']['buttons'] = [
            {
                'title': 'Поехать на рабочее место',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'не проводить допрос':
        res['response']['text'] = '''
            Вы решили не допрашивать Ребекку, а вместо этого пойти перекусить.'''
        res ['response']['buttons'] = [
            {
                'title': 'Поехать на рабочее место',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'поехать на рабочее место':
        rassled2(res, req)
    return


def rassled2(res, req):
    res['response']['text'] = '''
        Бонни Уинтерботтом смогла достать запись допроса Ребекки Саттер, на которой видно, что показания она давала под давлением. Теперь у стороны защиты будет больше шансов обеспечить выход девушки под залог.
        На заседании сторона обвинения предоставила сфабрикованную версию записи допроса, а сторона защиты – настоящую. Судья установил залог в 100 000 долларов на освобождение Ребекки Саттер и внутреннюю проверку в отношении следователя, который вёл допрос.'''
    res['response']['buttons'] = [
        {
            'title': 'Спустя несколько часов',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'спустя несколько часов':
        res['response']['text'] = '''
            Вечером к вам домой заявился Уэс Гиббинс. Он принёс мобильный телефон Лайлы Стэнгард, который спрятала у него дома Ребекка. В телефоне вы обнаружили некоторые фотографии, подтверждающие, что у Сэма Киттинга были с ней близкие отношения.
	        Вы сообщили об этом Аннализ.'''
        res['response']['buttons'] = [
            {
                'title': 'Продолжить расследование',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'продолжить расследование':
        next(res, req)
    return


def next(res, req):
    res['response']['text'] = '''
        Ваше расследование продолжается. Что будете делать дальше?'''
    res['response']['buttons'] = [
        {
            'title': 'Допросить Сэма',
            'hide': True
            },
        {
            'title': 'Пригласить Сэма в качестве психолога',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'допросить сэма':
        res['response']['text'] = '''
            По словам Сэма Киттинга, в ночь убийства Лайла Стэнгард звонила ему и умоляла  приехать, поэтому он отменил лекцию и поехал в Филадельфию, но не смог найти свою любовницу, и вернулся обратно в Нью-Хейвен. Киттинг клянётся, что не убивал её.'''
        res['response']['buttons'] = [
            {
                'title':'Перекусить',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'пригласить сэма в качестве психолога':
        res['response']['text'] = '''
            Вы пригласили Сэма для того, чтобы с его помощью выведать у Ребекки Саттер всё, что Лайла Стэнгард когда-либо про него говорила.
	        Ребекка и Лайла познакомились в баре. Избалованной Лайле не хватало острых ощущений, и она напросилась торговать наркотиками. Клиентами были другие студенты, в основном – девочки из Каппа Каппа Тета.

	        За ночь до своего исчезновения Лайла сказала, что завязывает с торговлей. Тогда же она и оставила свой телефон в квартире Саттер.
	        Лайла рассказывала подруге о своём любовнике. Она называла его мистер Дарси, но никаких подробностей, кроме того, что он женат, не раскрывала. Сама же Ребекка сказала, что он – просто старик, заскучавший в браке, Лайле это надоело, и поэтому она его бросила. В отместку он её убил.'''
        res['response']['buttons'] = [
            {
                'title':'Поехать и перекусить',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'перекусить':
        part2(res, req)
    elif req['request']['original_utterance'].lower() == 'поехать и перекусить':
        part1(res, req)
    return


def part1(res, req):
    res['response']['text'] = '''
        Позже в тот же день Ребекка Саттер сбежала.
        Она догадалась, кто такой мистер Дарси, и решила, что не может никому верить.
        Итак, что же вы будете делать дальше?'''
    res['response']['buttons'] = [
        {
            'title': 'Вызовать на допрос Гриффина О’Райли',
            'hide': True
            },
        {
            'title': 'Попробовать выяснить, где сейчас Ребекка',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'вызовать на допрос гриффина о’райли':
        res['response']['text'] = '''
            Гриффин сказал, что за два дня до убийства Лайлы он узнал, что она ему изменяла и ещё несколько дней пил, не просыхая. Что он делал в это время, не помнит. Помнит только, что был очень взбешён и был готов убить каждого, кто бы его ещё хоть каплю разозлил.'''
        res['response']['buttons'] = [
            {
                'title': 'Отправиться домой спать',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'отправиться домой спать':
        pobeg1(res, req)
    elif req['request']['original_utterance'].lower() == 'попробовать выяснить, где сейчас ребекка':
        pobeg2(res, req)
    return


def part2(res, req):
    res['response']['text'] = '''
        Позже в тот же день Ребекка Саттер сбежала.
	    Она догадалась, кто такой мистер Дарси, и решила, что не может никому верить.
		Итак, что же вы будете делать дальше?'''
    res['response']['buttons'] = [
        {
            'title': 'Вызову на допрос Гриффина О’Райли',
            'hide': True
            },
        {
            'title': 'Попробую выяснить, где сейчас Ребекка',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'вызову на допрос гриффина о’райли':
        sec_end(res, req)
    elif req['request']['original_utterance'].lower() == 'попробую выяснить, где сейчас ребекка':
        pobeg2(res, req)
    return


def pobeg1(res, req):
    res['response']['text'] = '''
        На следующий день она вернулась. В новостях Ребекка увидела, что у полиции новый главный подозреваемый, - Гриффин О’Райли'''
    res['response']['buttons'] = [
        {
            'title': 'Отправиться в суд',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'отправиться в суд':
        sud(res, req)
    return


def pobeg2(res, req):
    res['response']['text'] = '''
        Студент Аннализ Уэс Гиббинс поехал за ней и убедил, что она будет в безопасности только, если не будет выкидывать подобных фокусов'''
    res['response']['buttons'] = [
        {
            'title': 'Поехать в суд',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'поехать в суд':
        sud(res, req)
    return


def sud(res, req):
    res['response']['text'] = '''
        В новостях всплыла информация, что у Гриффина О’Райли и Ребекки Саттер были отношения, и что в ночь убийства Лайлы они были вместе.
	    Ребекка подтвердила, что Лайла застукала их вдвоём, но уверяет вас, что между ней и Гриффином до и после той ночи ничего не было.
	    На заседании судья выдала право молчания, запрещающее подозреваемым и их законным представителям общаться с прессой.
	    Также, на заседании адвокат Гриффина, Киган, предоставил улики, не замеченные ранее, а именно – следы от ногтей на шее Лайлы Стэнгард и заявил о своём намерении эксгумировать её тело и провести повторную экспертизу. Он уверен, что это укажет на Ребекку как на убийцу.
	    Что будете делать теперь?'''
    res['response']['buttons'] = [
        {
            'title': 'Найду улики, чтобы дискредитировать Кигана и его эксперта',
            'hide': True
            },
        {
            'title': 'Узнаю, кто слил информацию в прессу',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'найду улики, чтобы дискредитировать кигана и его эксперта':
        res['response']['text'] = '''
            Вы покопались в архивах и нашли дело «Штат против Холдена», в котором участвовал тот же эксперт, доктор Тёрнер. Также вы нашли письмо окружного прокурора, в котором он излагал свои сомнения по поводу методов Тёрнера.
	        Что теперь?'''
        res['response']['buttons'] = [
        {
            'title': 'Передам материалы Аннализ',
            'hide': True
            },
        {
            'title': 'Постараюсь убедить родителей Лайлы запретить эксгумацию её тела',
            'hide': True
            }
        ]
    elif req['request']['original_utterance'].lower() == 'передам материалы аннализ':
        res['response']['text'] = '''Вы передали материалы Аннализ. Теперь вам остаётся только ждать завтрашнего слушания'''
        res['response']['buttons'] = [
            {
                'title': 'Ждать',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'ждать':
        best_end(res, req)
    elif req['request']['original_utterance'].lower() == 'постараюсь убедить родителей лайлы запретить эксгумацию её тела':
        third_end(res, req)
    elif req['request']['original_utterance'].lower() == 'узнаю, кто слил информацию в прессу':
        best_end(res, req)
    return


def bar(res, req):
    res['response']['text'] = '''
        Вы решили поехать в ваш любимый бар, но он оказался закрыт. Вы развернулись и поехали домой.'''
    res['response']['buttons'] = [
        {
            'title': 'Следующий день',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == 'следующий день':
        prison2(res, req)
    return


def first_end(res, req):
    res['response']['text'] = '''
        Приехав в офис вы обнаружили, что для того, чтобы заполучить запись, Бонни Уинтерботтом сдала ваш незаконный обыск машины Сэма Киттинга вашему начальнику. Вы уволены с работы.

        Хотите начать сначала или посмотреть сериал, по мативам которого была создана игра?'''
    res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                },
            {
                'title': 'Посмотреть сериал, по мативам которого была создана игра',
                'payload': {},
                'url': 'https://www.kinopoisk.ru/film/kak-izbezhat-nakazaniya-za-ubiystvo-2014-804876/',
                'hide': True
                }
            ]
    if req['request']['original_utterance'].lower() == 'посмотреть сериал, по мативам которого была создана игра':
        res['response']['text'] = 'Приятного просмотра'
    return

def sec_end(res, req):
    res['response']['text'] = '''
        Гриффин сказал, что за два дня до убийства Лайлы он узнал, что она ему изменяла и ещё несколько дней пил, не просыхая. Что он делал в это время, не помнит. Помнит только, что был очень взбешён и был готов убить каждого, кто бы его ещё хоть каплю разозлил.

        Расследование зашло в тупик.
       Хотите начать сначала или посмотреть сериал, по мативам которого была создана игра?'''
    res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                },
            {
                'title': 'Посмотреть сериал, по мативам которого была создана игра',
                'payload': {},
                'url': 'https://www.kinopoisk.ru/film/kak-izbezhat-nakazaniya-za-ubiystvo-2014-804876/',
                'hide': True
                }
            ]
    if req['request']['original_utterance'].lower() == 'посмотреть сериал, по мативам которого была создана игра':
        res['response']['text'] = 'Приятного просмотра'
        res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'начать сначала':
        play_game(res, req)
    return


def third_end(res, req):
    res['response']['text'] = '''
        Вы смогли убедить миссис Стэнгард, что адвокат Гриффина хочет запутать улики и освободить своего клиента, привели в пример три других дела, когда он поступал точно так же, и его подзащитных освобождали.
        Вы сыграли на том, что мистер и миссис Стэнгард не доверяли Гриффину и были всячески против их с Лайлой союза. Миссис Стэнгард написала заявление, что она против эксгумации, но ничего ещё не закончено.


        Аннализ предоставила все имеющиеся у неё улики и доказательства на заседании. Суд не спешит принимать решение.
        На следующем заседании государственный обвинитель предоставила отчёт третьего эксперта, из которого следовало, что отметины на шее убитой очень похожи на следы женских ногтей.
        Суд запретил эксгумацию тела. Ни одна из сторон больше не смогла предоставить никаких доказательств и в связи с нехваткой улик – дело приостановлено.

        Хотите начать сначала или посмотреть сериал, по мативам которого была создана игра?'''
    res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                },
            {
                'title': 'Посмотреть сериал, по мативам которого была создана игра',
                'payload': {},
                'url': 'https://www.kinopoisk.ru/film/kak-izbezhat-nakazaniya-za-ubiystvo-2014-804876/',
                'hide': True
                }
            ]
    if req['request']['original_utterance'].lower() == 'посмотреть сериал, по мативам которого была создана игра':
        res['response']['text'] = 'Приятного просмотра'
        res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'начать сначала':
        play_game(res, req)
    return


def best_end(res, req):
    res['response']['text'] = '''
            На следующем заседании государственный обвинитель предоставила отчёт своего эксперта, из которого следовало, что отметины на шее убитой очень похожи на следы женских ногтей.
            У вас не получилось узнать, кто же сливал в прессу информацию, но вы нашли кое-что получше.

            Адвокат Гриффина О’Райли сговорился с государственным обвинителем: если она поддерживает его версию о том, что отметины на шее Лайлы Стэнгард – это следы ногтей, то она получит очень хорошее повышение в должности.
            Ребекка предложила Аннализ нарушить право молчания и сделать вброс в прессу, о том, что Гриффин её опоил и, пока она была без сознания, использовал.'''
    res['response']['buttons'] = [
        {
            'title': '-->',
            'hide': True
            }
        ]
    if req['request']['original_utterance'].lower() == '-->':
        res['response']['text'] = '''
            Учитывая все обстоятельства дела, судья выдала распоряжение провести немедленную эксгумацию тела Лайлы.
	        При повторной экспертизе выяснилось, что следы на шее Лайлы – это укусы муравьёв.
	        Но также была выявлена деталь, упущенная в первый раз: девушка была на шестой неделе беременности.
	        Безо всякого сомнения, всё встало на свои места. Сэм Киттинг очень дорожил своим браком с Аннализ, как-никак, они были женаты более двадцати лет. Конечно, он грешил интрижками на стороне, но всё это было из-за того, что его жена не могла иметь ребёнка после двух выкидышей. Сэм очень сильно переживал и за неё, и за себя, и – за их брак.'''

        res['response']['buttons'] = [
            {
                'title': 'Продолжать заседание',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'продолжать заседание':
        res['response']['buttons'] = '''
	        Но в случае с Лайлой ему не повезло. Девушка забеременела и категорически отказывалась делать аборт. Сэм пытался её переубедить, но она его не слушала. Лайла хотела пойти к Аннализ и всё ей рассказать. Наивная студентка думала, что Сэм будет любить её и их ребёнка, и ради них уйдёт из семьи. Но она ошибалась.
	        В ту роковую ночь, Лайла поняла, что больше не будет ждать. Она поставила Сэму ультиматум: либо он сейчас же возвращается в Филадельфию и уходит от жены, либо это делает она. Киттинг не мог позволить этому случиться. Он отменил лекцию в Йеле и примчался так быстро, как только смог. Лайла ждала его на крыше кампуса. Он думал, что сможет образумить свою любовницу, но у него не вышло. Тогда Сэм понял, что у него есть только один способ решить эту проблему.

	        И он убил Лайлу Стэнгард.
	        На допросе Сэм всё подтвердил.
	        Поздравляем, детектив, вы раскрыли дело!

	        Хотите начать сначала или посмотреть сериал, по мативам которого была создана игра?'''
        res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                },
            {
                'title': 'Посмотреть сериал, по мативам которого была создана игра',
                'payload': {},
                'url': 'https://www.kinopoisk.ru/film/kak-izbezhat-nakazaniya-za-ubiystvo-2014-804876/',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'посмотреть сериал, по мативам которого была создана игра':
        res['response']['text'] = 'Приятного просмотра'
        res['response']['buttons'] = [
            {
                'title': 'Начать сначала',
                'hide': True
                }
            ]
    elif req['request']['original_utterance'].lower() == 'начать сначала':
        play_game(res, req)
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
