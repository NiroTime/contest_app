tests = {
    0: True,
    10: True,
    9: 9,
    511: 1,
}


def testing(tests, func):
    try:
        for test, answer in tests.items():
            if func(test) != answer:
                return(f'Тест: {test}, не пройден. '
                       f'Ваш результат: {func(test)} '
                       f'Ожидаемый результат: {answer}'
                       )
        return 'Тесты пройдены!'
    except Exception as err:
        return err
