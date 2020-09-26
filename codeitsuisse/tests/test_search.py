from codeitsuisse.routes.slms import Solution


def test_ladder():
    n = 10
    p = 1
    j = ["4:6"]
    s = Solution(n, p, j)
    print(s.search())


def test_snake():
    n = 10
    p = 1
    j = ["6:4"]
    s = Solution(n, p, j)
    result = [r.value for r in s.search()]
    assert result in [[3, 6]]


def test_smoke():
    n = 10
    p = 1
    j = ["7:0"]
    s = Solution(n, p, j)
    result = [r.value for r in s.search()]
    assert result in [[3, 6]]


def test_mirror():
    n = 10
    p = 1
    j = ["0:4"]
    s = Solution(n, p, j)
    result = [r.value for r in s.search()]
    assert result in [[3, 6]]


def test_small():
    n = 20
    p = 1
    j = ["16:6", "10:19", "0:13", "14:0"]
    s = Solution(n, p, j)
    print(s.search())


def test_A():
    n = 64
    p = 3
    j = ["0:39", "8:37", "0:15", "5:50", "52:0", "19:29", "35:0", "47:45", "18:0", "53:44", "0:36", "46:2"]
    s = Solution(n, p, j)
    print(s.get_rolls())
