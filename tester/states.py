from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    start_test = State()