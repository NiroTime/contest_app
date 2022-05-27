tests = {
    (1,8,6,2,5,4,8,3,7): 49,
    (1,1): 1,
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
