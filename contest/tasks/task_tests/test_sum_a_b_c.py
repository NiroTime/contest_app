tests = {
    (1, 2, 3): 6,
    (0, 0, 0): 0,
    (-1, -2, -3): -6,
}


def testing(tests, func):
    try:
        for test, answer in tests.items():
            if func(*test) != answer:
                return(f'Тест: {test}, не пройден. '
                       f'Ваш результат: {func(*test)} '
                       f'Ожидаемый результат: {answer}'
                       )
        return 'Тесты пройдены!'
    except Exception as err:
        return err
