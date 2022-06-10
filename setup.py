import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsp",
    version="0.0.1",
    author="André L. Maravilha",
    author_email="andre.maravilha@cefetmg.br",
    description="Python code with different MIP models implemented for the TSP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andremaravilha/tsp-formulations",
    packages=setuptools.find_packages(),
    requires=["tsplib95", "matplotlib", "gurobipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)