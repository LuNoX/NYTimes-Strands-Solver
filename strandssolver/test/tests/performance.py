import cProfile
from pstats import SortKey


def test() -> None:
    from strandssolver.test.stubs.stubdictionarytrie import _test
    _test()


def main() -> None:
    cProfile.run("test()", sort=SortKey.TIME)


if __name__ == '__main__':
    main()
