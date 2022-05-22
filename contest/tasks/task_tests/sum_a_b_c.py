from .form_answer import sum_a_b_c

tests = {
    (1, 2, 3): 6,
    (0, 0, 0): 0,
    (-1, -2, -3): -6,
}


def testing():
    try:
        for test, answer in tests.items():
            if sum_a_b_c(*test) != answer:
                return(f'Тест: {test}, не пройден. '
                       f'Ваш результат: {sum_a_b_c(*test)} '
                       f'Ожидаемый результат: {answer}'
                       )
        return 'Тесты пройдены!'
    except Exception as err:
        return err
