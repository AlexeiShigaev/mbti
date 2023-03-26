from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from mbti.calculates import calculate_and_return_result
from loader import bot
from logs import logger
from mbti.texts import mbti_info, mbti_test, QUESTIONS_COUNT
from tester.states import UserState
import numpy as np



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    """Реагирует на команду start"""
    logger.info('Получена команда {}\n{}'.format(message.text, message))

    mess = bot.send_message(
        message.chat.id,
        "Привет, {}\n{}".format(message.from_user.first_name, mbti_info),
        reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton('Начинаем', callback_data='answer:-1:a'))
    )
    """Обнуляем базу ответов."""
    bot.set_state(message.from_user.id, UserState.start_test, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['results'] = np.array([['' for i in range(7)] for j in range(10)])
    logger.info('{}: Отправлено send_message:\n{}'.format(message.text[1:], mess))



@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    """Дэфолтная реакция на любые сообщения"""
    logger.info('get_text_messages\n{}'.format(message))

    if message.text.lower().startswith('привет'):
        bot.reply_to(message, "Привет")
    else:
        bot.reply_to(message, "Моя-твоя-не-понимай\nКоманда /help")


@bot.message_handler(func=lambda param: param.startswith('/'))
def reply_default_command(message: Message):
    """Дэфолтная реакция на любую команду, не обработанную до этого момента."""
    logger.info('reply_default_command\n{}'.format(message))
    bot.reply_to(message, "Команда не реализована")


"""Блок связанный с обработкой ответов на опросник"""

def gen_question(index: int):
    # print('gen_question number {}'.format(index))
    if 0 > index >= QUESTIONS_COUNT:
        raise Exception('Bad index for question {}'.format(index))
    return ["Вопрос {} из 70\n{}".format(index + 1, mbti_test[index][0]),
                quick_markup({
                    mbti_test[index][1]: {'callback_data': 'answer:{}:a'.format(index)},
                    mbti_test[index][2]: {'callback_data': 'answer:{}:b'.format(index)}
                }, row_width=1)
            ]


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('answer'))
def answer_callback(call: CallbackQuery):
    """Начинаем задавать вопросы. Ловит все ответы на вопросы."""
    logger.info('Задаем вопрос: {}'.format(call.message))

    """Выделим номер отвеченного вопроса и зафиксируем ответ."""
    lst = call.data.split(':')
    if len(lst) < 3:
        """Косяк возможен, хотя и маловероятен"""
        raise Exception('answer_callback: Bad answer {}'.format(call.data))

    question_index = int(lst[1])
    print('question_index={}'.format(question_index))

    """Если ответ ожидаемый, фиксируем ответ"""
    if 0 <= question_index < QUESTIONS_COUNT:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['results'][question_index // 7][question_index % 7] = lst[2]
            print(data['results'])

    """Дойдя до последнего вопроса/ответа выдаем результат опроса"""
    if question_index == (QUESTIONS_COUNT - 1):
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(
                call.message.chat.id, calculate_and_return_result(data['results']),
            )
        logger.info('Опрос закончен')
        return

    """А если это не конец,переходим к следующему вопросу"""
    question_index += 1
    question_index = max(question_index, 0)
    question_index = min(question_index, QUESTIONS_COUNT - 1)

    """заменим сообщение и кнопки на главое меню"""
    question = gen_question(question_index)
    bot.edit_message_text(
        question[0],
        call.message.chat.id, call.message.id# , parse_mode='HTML'
    )
    """и кнопки тоже"""
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=question[1]
    )
    logger.info('Отправили вопрос {} и варианты ответов'.format(question_index))


@bot.callback_query_handler(func=None)
def default_handler(call: CallbackQuery):
    """Заглушка. Дэфолтный обработчик callback_query. Нужен больше для процесса разработки"""
    print('default_handler:' + call.data)
    print(call)
