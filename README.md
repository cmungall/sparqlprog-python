# sparqlprog for python

wraps [sparqlprog](https://github.com/cmungall/sparqlprog)



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

You can then pass `http://localhost:9083` as the service URL parameter


