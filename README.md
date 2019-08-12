# sparqlprog for python

This module wraps
[sparqlprog](https://github.com/cmungall/sparqlprog), providing a
Python API for executing logic program queries over SPARQL endpoints.

Example:

```python
from prologterms import TermGenerator, PrologRenderer, Program, Var
from sparqlprog import SPARQLProg
P = TermGenerator()

S = SPARQLProg(endpoint='wd')
C = Var('C')
N = Var('N')
query = (P.continent(C), P.enlabel(C, N))
for r in S.query(query):
    print(f"{r['C']} {r['N']}")
```

## Example Notebook

See [Notebook_01_Basics.ipynb](Notebook_01_Basics.ipynb)

## Installation

To install

    python3 -m venv venv
    source venv/bin/activate
    export PYTHONPATH=.:$PYTHONPATH
    pip install -r requirements.txt 

You will need access to a sparqlprog service. You can use the public
one on Heroku (default) or run your own.

Running your own is easy if you have Docker:

    docker run -p 9083:9083 cmungall/sparqlprog

You can then pass `http://localhost:9083` as the service URL parameter. E.g

Query wikidata for continents and their names:

   ./sparqlprog.py  -u http://localhost:9083 -e wd "continent(X), enlabel(X,N)" 

You can also use the default service on heroku, but it is not guaranteed to be running:

   ./sparqlprog.py  -e wd "continent(X), enlabel(X,N)" 


