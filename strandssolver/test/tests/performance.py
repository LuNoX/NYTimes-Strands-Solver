import cProfile


def test() -> None:
    print(1)
    from strandssolver.test.stubs import stubgraph
    from strandssolver.test.stubs import stubgamestate
    from strandssolver.test.stubs import stubdictionarytrie

    graph = stubgraph.StubGraphBuilder.build_graph_from_board()


def main() -> None:
    cProfile.run("test()")


if __name__ == '__main__':
    main()
