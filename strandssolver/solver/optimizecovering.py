from __future__ import annotations

import numpy as np
import numpy.typing
import nptyping
import pulp
import networkx as nx

from typing import Callable, Iterable, Tuple


class BinaryOptimizer:
    """
    Optimizes the residual for a binary problem of the form:
        r = Ax - b
    r: the (n x 1) residual vector
    A: the (n x m) binary problem matrix
    x: the (m x 1) binary input vector
    b: the (n x 1) binary target vector
    """
    type ProblemType = nptyping.NDArray[nptyping.Shape["*, *"], nptyping.Bool]
    type InputType = nptyping.NDArray[nptyping.Shape["*"], nptyping.Bool]
    type TargetType = nptyping.NDArray[nptyping.Shape["*"], nptyping.Bool]
    type ResidualType = BinaryOptimizer.TargetType

    DEFAULT_NORM = pulp.lpSum

    def __init__(self, problem: ProblemType = None, target: TargetType = None,
                 norm: Callable[[ResidualType], float] = None) -> None:
        self._target: BinaryOptimizer.TargetType = None
        self.target = target
        self._problem: BinaryOptimizer.ProblemType = None
        self.problem = problem
        if norm is None:
            norm = BinaryOptimizer.DEFAULT_NORM
        self.norm = norm

    @property
    def target(self) -> BinaryOptimizer.TargetType:
        if self._target is None:
            raise ValueError("b has not been set yet!")
        return self._target

    @target.setter
    def target(self, target: np.typing.ArrayLike | BinaryOptimizer.TargetType
               ) -> None:
        if not isinstance(target, nptyping.NDArray[nptyping.Shape["*"],
        nptyping.Bool]):
            target = np.array(target, dtype=np.bool_)
        self._target = target

    @property
    def problem(self) -> BinaryOptimizer.ProblemType:
        if self._problem is None:
            raise ValueError("A has not been set yet!")
        return self._problem

    @problem.setter
    def problem(self,
                problem: np.typing.ArrayLike | BinaryOptimizer.ProblemType
                ) -> None:
        if not isinstance(problem, nptyping.NDArray[nptyping.Shape["*, *"],
        nptyping.Bool]):
            problem = np.array(problem, dtype=np.bool_)
        if problem.ndim != 2:
            shape = (self.target.shape[0], -1)
            problem = problem.reshape(shape)
        self._problem = problem

    def optimize_binary_vector(self) -> BinaryOptimizer.InputType:
        A = self.problem
        b = self.target
        n, m = A.shape

        optimization = pulp.LpProblem("Binary_Optimization", pulp.LpMinimize)
        x = [pulp.LpVariable(f'x_{i}', cat=pulp.LpBinary) for i in range(m)]
        # Define the residual vector r = Ax - b
        residuals = [pulp.lpSum(A[i, j] * x[j] for j in range(m)) - b[i]
                     for i in range(n)]

        residuals_abs = [pulp.LpVariable(f'r_abs_{i}', lowBound=0)
                         for i in range(m)]

        for i in range(m):
            optimization += residuals_abs[i] >= residuals[i]
            optimization += residuals_abs[i] >= -residuals[i]

        objective = self.norm(residuals_abs)
        optimization += objective

        optimization.solve()

        return np.array(x, dtype=np.bool_)


def convert_words_to_problem_matrix(words: Iterable[Tuple[Tuple[int, ...]]],
                                    graph: nx.Graph
                                    ) -> BinaryOptimizer.ProblemType:
    nodes = list(graph.nodes)
    index_per_node = {node: index for index, node in enumerate(nodes)}
    problem = []
    for word in words:
        vector = np.zeros(len(nodes), dtype=np.bool_)
        node_indices_in_word = [index_per_node[node] for node in word]
        vector = vector[node_indices_in_word] = True
        problem.append(vector)
    return problem


def convert_problem_solution_to_words(solution: BinaryOptimizer.InputType,
                                      words: Iterable[Tuple[Tuple[int, ...]]]
                                      ) -> Iterable[Tuple[Tuple[int, ...]]]:
    return [word for include, word in zip(solution, words) if include]


def _test() -> None:
    # Example usage
    A = [[1, 0, 1],
         [0, 0, 1],
         [1, 1, 0]]

    b = [1, 1, 1]

    optimizer = BinaryOptimizer(problem=A, target=b)
    x_optimal = optimizer.optimize_binary_vector()
    print("Optimal x:", x_optimal)


if __name__ == "__main__":
    _test()
