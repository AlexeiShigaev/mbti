import sys
from time import sleep

import requests
import loader
from tester.commands import *


if __name__ == '__main__':
    logger.info('Запуск')
# loader.bot.polling(none_stop=True, interval=0)
    while True:
        try:
            loader.bot.polling(none_stop=True, interval=0)
        except requests.exceptions.ReadTimeout as ex:
            tb = sys.exc_info()[2]
            logger.error('\nПроизошло исключение ReadTimeout\n{}'.format(str(ex.with_traceback(tb))))
        except Exception as ex:
            tb = sys.exc_info()[2]
            logger.error('\nПроизошло исключение2\n{}'.format(str(ex.with_traceback(tb))))
        finally:
            sleep(5)
            logger.info('Попытка перезапуска после исключения')