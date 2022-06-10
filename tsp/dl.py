import gurobipy as gp
from gurobipy import GRB


def add_subtour_constraints(problem, model, x, get_node_id, get_node_index):
    """ Desrochers and Laporte (DL) formulation.
        
        Reference:
        DESROCHERS, M.; LAPORTE, G.; Improvements and extensions to the Miller-
        Tucker-Zemlin subtour elimination constraints. Operations Research 
        Letters, v. 10, pp. 27-36, 1991.
    """

    # Dimension of the problem (number of nodes)
    n = problem.dimension

    # Create additional u[i] continuous decision variables
    u = [model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS) for i in range(0, n)]

    for i in range(1, n):
        for j in range(1, n):
            model.addConstr(u[i] - u[j] + (n - 1) * x[i][j] + (n - 3) * x[j][i] <= n - 2)

    for i in range(1, n):
        lb = gp.LinExpr()
        ub = gp.LinExpr()

        lb = lb + 1 + (n - 3) * x[i][0]
        ub = ub + n - 1 - (n - 3) * x[0][i]

        for j in range(1, n):
            lb = lb + x[j][i]
            ub = ub - x[i][j]

        model.addConstr(u[i] >= lb)
        model.addConstr(u[i] <= ub)

    # Fix u[0] to 0 (zero)
    model.addConstr(u[0] == 0)
