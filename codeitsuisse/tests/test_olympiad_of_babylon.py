from codeitsuisse.routes.olympiad_of_babylon import olympiad_of_babylon


def test_intelligent_farming():
    num_books = 5
    num_days = 3
    books = [114, 111, 41, 62, 64]
    days = [157, 136, 130]

    expected = 5
    actual = olympiad_of_babylon(num_books, num_days, books, days)
    assert actual == 5
