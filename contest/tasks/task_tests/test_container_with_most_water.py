from .form_answer import container_with_most_water

tests = {
    (1,8,6,2,5,4,8,3,7): 49,
    (1,1): 1,
}


def testing():
    try:
        for test, answer in tests.items():
            if container_with_most_water(test) != answer:
                return(f'Тест: {test}, не пройден. '
                       f'Ваш результат: {container_with_most_water(test)} '
                       f'Ожидаемый результат: {answer}'
                       )
        return 'Тесты пройдены!'
    except Exception as err:
        return err
