import argparse
from os import path
from importlib.machinery import SourceFileLoader
import tsplib95
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB


def _main():

    # Configure the command line argument parser
    parser = argparse.ArgumentParser(prog="tsp", description="Program with some MIP models for the TSP.")
    parser.add_argument('--model', type=str, required=True, help='name of the MIP model to use')
    parser.add_argument('--display', action='store_true', help='display the incumbent solution along the optimization process')
    parser.add_argument('--no-log',  action='store_true', help='disable Gurobi logging of the optimization process')
    parser.add_argument('file', metavar="FILE", type=str, help='path to the instance file')
    args = parser.parse_args()

    # Load TSP instance data
    problem = tsplib95.load(args.file)

    node_id = [i for i in problem.get_nodes()]
    get_node_id = lambda index: node_id[index]
    get_node_index = lambda id: node_id.index(id)
    
    # Initialize Gurobi model
    model = gp.Model()
    
    if args.no_log:
        model.setParam(GRB.Param.LogToConsole, 0)

    # Create x[i][j] binary decision variables
    x = [[model.addVar(lb=0, ub=1, vtype=GRB.BINARY) for j in range(0, problem.dimension)] 
         for i in range(0, problem.dimension)]

    # Set objective function
    objective = gp.LinExpr()
    for i in range(0, problem.dimension):
        for j in range(0, problem.dimension):
            objective = objective + problem.get_weight(get_node_id(i), get_node_id(j)) * x[i][j]

    model.setObjective(objective, GRB.MINIMIZE)

    # Add common constraints (self-loops, incoming arcs, outgoing arcs)
    for i in range(0, problem.dimension):
        arcs_in = gp.LinExpr()
        arcs_out = gp.LinExpr()
        for j in range(0, problem.dimension):
            arcs_in = arcs_in + x[j][i]
            arcs_out = arcs_out + x[i][j]
        
        model.addConstr(x[i][i] == 0)
        model.addConstr(arcs_in == 1)
        model.addConstr(arcs_out == 1)
    
    # Load module that implements subtour elimination constraints
    source_dir = path.dirname(path.abspath(__file__))
    source_file = args.model + '.py'
    source_path = path.join(source_dir, source_file)
    subtour_module = SourceFileLoader(args.model, source_path).load_module()

    # Add subtour elimination constraints into the model
    subtour_module.add_subtour_constraints(problem, model, x, get_node_id, get_node_index)

    # Solve the problem
    if args.display and problem.edge_weight_type in ['EUC_2D', 'ATT']:
        callback = lambda _, where: _callback(problem, model, x, get_node_id, get_node_index, where)
        model.optimize(callback)
    else:
        model.optimize()

    # Display info about MIP formulation
    print(f'')
    print(f'-----------------------------------------------------------')
    print(f'Info about the MIP formulation')
    print(f'-----------------------------------------------------------')
    print(f'Number of decision variables: {model.numVars}')
    print(f'Number of constraints: {model.numConstrs}')
    print(f'')

    # Display info about the optimization problem
    print(f'-----------------------------------------------------------')
    print(f'Info about the optimization process')
    print(f'-----------------------------------------------------------')
    print(f'B&C nodes explored: {model.nodeCount}')
    print(f'Simplex iterations: {model.iterCount}')
    print(f'MIP gap: {model.mipGap if model.mipGap != GRB.INFINITY else "unavailable"}')
    print(f'Elapsed time (s): {model.runtime:.4f}')
    print(f'')

    # Display the best solution, if any
    print(f'-----------------------------------------------------------')
    print(f'Info about the best solution found')
    print(f'-----------------------------------------------------------')
    if model.solCount == 0:
        print(f'No solution found!\n')

    else:

        # Get the best tour found and its value of objective function
        xval = [[x[i][j].X for j in range(0, problem.dimension)]
            for i in range(0, problem.dimension)]

        tour = _get_tour(problem, xval, get_node_id, get_node_index)
        objval = model.objVal

        print(f'Is optimal: {"Yes" if model.status == GRB.OPTIMAL else "No"}')
        print(f'Cost: {model.objVal}')
        print(f'Tour: {tour}')
        print(f'')

        # Draw the tour
        if args.display and problem.edge_weight_type in ['EUC_2D', 'ATT']:
            _draw_tour(problem, tour, objval, block=True, interactive=False, show=True)


def _callback(problem, model, x, get_node_id, get_node_index, where):
    
    # Check if callback is due to a new incumbent solution
    if where == GRB.Callback.MIPSOL:

        # Get current solution and its value of objective function
        xval = [[model.cbGetSolution(x[i][j]) for j in range(0, problem.dimension)]
                for i in range(0, problem.dimension)]

        objval = model.cbGet(GRB.Callback.MIPSOL_OBJ)

        # Find and draw tour
        tour = _get_tour(problem, xval, get_node_id, get_node_index)
        _draw_tour(problem, tour, objval, block=False, interactive=False, show=True)


def _get_tour(problem, xval, get_node_id, get_node_index):
    tour = []
    current = 0
    next = None

    while next != 0:
        for j in range(0, problem.dimension):
            if xval[current][j] > 0.5:
                next = j
        tour.append(get_node_id(current))
        current = next

    tour.append(tour[0])    
    return tour


def _draw_tour(problem, tour, cost=None, figure_id="tsp-tour", block=True, interactive=False, show=True):
    if problem.edge_weight_type not in ['EUC_2D', 'ATT']:
        raise Exception('Problem data not support graphical display')

    # Get node's coordinates
    coordinates = {i: tuple(problem.get_display(i)) for i in problem.get_nodes()}
    
    nodes_x = [coordinates[i][0] for i in problem.get_nodes()]
    nodes_y = [coordinates[i][1] for i in problem.get_nodes()]

    arcs_x = [coordinates[i][0] for i in tour]
    arcs_y = [coordinates[i][1] for i in tour]

    # Set interactivity on plot
    if interactive:
        plt.ion()
    else:
        plt.ioff()

    # Create (or activate) a figure
    plt.figure(figure_id, figsize=(7, 7), clear=True)

    # Draw the tour and nodes
    plt.plot(arcs_x, arcs_y)
    plt.scatter(nodes_x, nodes_y)

    # Show tour cost
    if cost is not None:
        plt.gcf().text(0.15, 0.90, f'Cost: {cost}', fontsize=14)

    # Axis labels
    plt.xlabel("x-coordinates", fontsize=14)
    plt.ylabel("y-coordinates", fontsize=14)
    
    # Show figure
    if show:
        plt.show(block=block)
        if not block:
            plt.pause(0.5)


if __name__ == "__main__":
    _main()
