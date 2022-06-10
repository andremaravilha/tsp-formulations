import gurobipy as gp
from gurobipy import GRB


def add_subtour_constraints(problem, model, x, get_node_id, get_node_index):
    """ Miller, Tucker and Zemlin (MTZ) formulation.
        
        Reference:
        MILLER, C.E.; TUCKER, A.W.; ZEMLIN, R.A. Integer programming formulations 
        and travelling salesman problems. Journal of the Association for Computing 
        Machinery, v.7, pp. 326-329, 1960.
    """

    # Dimension of the problem (number of nodes)
    n = problem.dimension

    # Create additional u[i] continuous decision variables
    u = [model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS) for i in range(0, n)]

    # Add MTZ subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            model.addConstr(u[i] - u[j] + (n - 1) * x[i][j] <= n - 2)

    # Add constraints that sets lower and upper bounds for u[i] variables
    for i in range(1, n):
        model.addConstr(u[i] >= 1)
        model.addConstr(u[i] <= n - 1)

    # Fix u[0] to 0 (zero)
    model.addConstr(u[0] == 0)
