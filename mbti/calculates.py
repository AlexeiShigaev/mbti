import numpy as np
from logs import logger
from mbti.texts import mbti_results


def calculate_and_return_result(answers: np.ndarray) -> str:
    param_e = sum(list(map(lambda el: 1 if el == 'a' else 0, answers[:, 0])))
    param_i = 10 - param_e
    print('E={}, I={}'.format(param_e, param_i))

    param_s = sum(list(map(lambda el: 1 if el == 'a' else 0, np.reshape(answers[0:, 1:3], 20))))
    param_n = 20 - param_s
    print('S={}, N={}'.format(param_s, param_n))

    param_t= sum(list(map(lambda el: 1 if el == 'a' else 0, np.reshape(answers[0:, 3:5], 20))))
    param_f = 20 - param_t
    print('T={}, F={}'.format(param_t, param_f))

    param_j = sum(list(map(lambda el: 1 if el == 'a' else 0, np.reshape(answers[0:, 5:7], 20))))
    param_p = 20 - param_j
    print('J={}, P={}'.format(param_j, param_p))

    result = ''

    result += 'E' if param_e > param_i else 'I'
    result += 'S' if param_s > param_n else 'N'
    result += 'T' if param_t > param_f else 'F'
    result += 'J' if param_j > param_p else 'P'

    print(result)
    if not result in mbti_results:
        logger.error('Нет кода {}'.format(result))
        return 'Что-то пошло не так\nВаш код {}'.format(result)

    return mbti_results[result]
