# Formulations for the (asymmetric) traveling salesman problem

> Prof. André L. Maravilha, D.Sc.  
> *Dept. of Informatics, Management and Design - Centro Fed. de Edu. Tecnológica de Minas Gerais ([url](https://www.cefetmg.br/))*  


## 1. Overview

This repository contains a Python implementation of different MIP formulations for the (asymmetric) traveling salesman problem (TSP) [1]. Its objective is just to show how different formulations for the same problem can vary in terms of size (number of decision variables and constraints), number of B&C nodes explored, and time for solution. All MIP formulations were written and solved with [gurobipy](https://pypi.org/project/gurobipy/), the Python API for [Gurobi Optimizer](https://www.gurobi.com/).


## 2. How to prepare your machine to run this project

Some important comments before starting to use this project:  
* This project was developed with Python 3.10 and the following modules: gurobipy (v. 9.5.1), tsplib95 (v. 0.7.1) and matplotlib (v. 3.5.2). Other requirements, and their respective versions, are listed at file `requirements.txt`.
* Command in sections bellow assumes your python executable is `python` and the Package Installer for Python (pip) is `pip`.
* Besides, it assumes the `venv` module is installed, since it will be used to build the Python Virtual Environment to run the project.
* As this project uses the `gurobipy` module, a license for Gurobi Optimizer is required. The Gurobi Optimizer license is not included with this project and must be obtained by the user.

### 2.1. Create and activate a Python Virtual Environment (venv)

First, you need to clone this repository or download it in your machine. Then, inside the root directory of the project, create a Python Virtual Environment (venv):
```
python -m venv ./venv
```

After that, you need to activate the virtual environment (venv) to run the `tsp` module.

In Linux machines, it is usually achieved by running the following command: 
```
source venv/bin/activate
```

On Windows:
```
.\venv\Scripts\activate
```

If you want to leave the virtual environment, simple run:
```
deactivate
```

### 2.2. Installing dependencies

Now that your virtual environment is installed, you need to install the dependencies required by this project: 
```
python -m pip install -r requirements.txt
```


## 3. Running the project

### 3.1. Show the help message of the program:

```
python -m tsp --help
```

### 3.2. General structure of the command line

```
python -m tsp --model MODEL [--display] [--no-log] FILE
```  
in which:  

`FILE`  
(Required)  
Path to the instance file of the TSP. This program supports the [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) format for symmetric and asymmetric traveling salesman problem.

`--model MODEL`  
(Required)
Name of the MIP formulation of the ATSP to use. Available values are:  
- `mtz` for Miller, Tucker and Zemlin (MTZ) formulation [2].
- `dl` for Desrochers and Laporte (DL) formulation [3].
- `dfj` for Dantzig, Fulkerson and Johnson (DFJ) formulation [4].

`--display`  
(Optional)
Show the incumbent tour along the optimization process. If the instance file does not contain the xy-coordinates of the nodes, this option is ignored.

`--no-log`  
(Optional)  
Disable Gurobi Optimizer logging of the optimization process.

### 3.3. Usage example
The directory `tsplib_example` contains some instances from the TSPLIB95 library to test the program. To get all instances from TSPLIB95, visit access the page [http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/).

```
python -m tsp --model mtz --display ./tsplib_example/att48.tsp
```  


## References
[1] Öncan, T.; Altınel, I. K.; Laporte, G. A comparative analysis of several asymmetric traveling salesman problem formulations. Computers & Operations Research, v. 36, pp. 637-654, 2009.

[2] Miller, C. E.; Tucker, A. W.; Zemlin, R. A. Integer programming formulations and travelling salesman problems. Journal of the Association for Computing Machinery, v.7, pp. 326-329, 1960.

[3] Desrochers, M.; Laporte, G.; Improvements and extensions to the Miller-Tucker-Zemlin subtour elimination constraints. Operations Research Letters, v. 10, pp. 27-36, 1991.

[4] Dantzig, G. B; Fulkerson, D. R.; Johnson, S. M. Solutions of a large-scale traveling-salesman problem. Operations Research, v. 2, pp. 363-410, 1954.
