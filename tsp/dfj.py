import itertools
import math
import gurobipy as gp
from gurobipy import GRB


def add_subtour_constraints(problem, model, x, get_node_id, get_node_index):
    """ Dantzig, Fulkerson and Johnson (DFJ) formulation.
        
        Reference:
        DANTZIG, G.B; FULKERSON, D.R.; JOHNSON, S.M. Solutions of a 
        large-scale traveling-salesman problem. Operations Research, 
        v. 2, pp. 363-410, 1954.
    """

    # Dimension of the problem (number of nodes)
    n = problem.dimension
    nodes = [i for i in range(1, n)]

    # Compute the number of DFJ subtour elimination constraints
    count = 0
    total = sum([math.comb(len(nodes), r) for r in range(2, n)])

    # Add DFJ subtour elimination constraints
    print(f'Creating DJF subtour elimination constraints... {count} of {total} ({(100*(count/total)):.2f}%) created.', end='')
    for r in range(2, n):
        for S in itertools.combinations(nodes, r):
            expr = gp.LinExpr()
            for i, j in itertools.permutations(S, 2):
                expr = expr + x[i][j]
            model.addConstr(expr <= len(S) - 1)

            count = count + 1
            print(f'\rCreating DJF subtour elimination constraints... {count} of {total} ({(100*(count/total)):.2f}%) created.', end='')

    print('')