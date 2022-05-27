from .form_answer import ostatok_ot_deleniya_na_10

tests = {
    0: True,
    10: True,
    9: 9,
    511: 1,
}


def testing():
    try:
        for test, answer in tests.items():
            if ostatok_ot_deleniya_na_10(test) != answer:
                return(f'Тест: {test}, не пройден. '
                       f'Ваш результат: {ostatok_ot_deleniya_na_10(test)} '
                       f'Ожидаемый результат: {answer}'
                       )
        return 'Тесты пройдены!'
    except Exception as err:
        return err
