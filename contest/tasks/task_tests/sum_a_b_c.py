from .form_answer import sum_a_b_c

tests = {
    (1, 2, 3): 6,
    (0, 0, 0): 0,
    (-1, -2, -3): -6,
}


def testing():
    for test, answer in tests.items():
        if sum_a_b_c(*test) != answer:
            return False
    return True
