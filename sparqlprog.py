#!/usr/bin/env python
"""
Module and command line utility for SPARQLProg
"""

from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine
from prologterms import TermGenerator, PrologRenderer, Program, Var, Term
from rdflib import Literal
import click
import logging

__author__ = "Chris Mungall <cjmungall@lbl.gov>"
__version__ = "0.0.2"

DEFAULT_SERVER = 'https://evening-falls-87315.herokuapp.com'

class SPARQLProg():
    """
    Wrapper for pengines to call a SPARQLProg service
    """

    def __init__(self,
                 server=DEFAULT_SERVER,
                 endpoint=None,
                 rules=None,
                 program=None):
        self.server = server
        self.endpoint = endpoint
        self.rules = rules
        self.renderer = PrologRenderer()
        if program is not None:
            if type(program) is not str:
                program = self.renderer.render(program)
        self.program = program
            

    def query(self, q, select=None, endpoint=None):
        """
        Query a sparqlprog endpoint

        Returns:
        iterator
        """
        P = TermGenerator()
        opts = []
        if self.rules is not None:
            # force a tuple
            opts = [P.rule( (r,) ) for r in self.rules]
        opts_str = self.renderer.render(opts)
        if select is None:
            select = q
        if select is not str:
            select = self.renderer.render(select)
        if type(q) is not str:
            q = self.renderer.render(q)
        if endpoint is None:
            endpoint = self.endpoint
        if endpoint is not None:
            q = f"'??'({endpoint}, ({q}), ({select}), {opts_str})"
        logging.info(f"Query={q}")
        logging.info(f"Program={self.program}")
        builder = PengineBuilder(urlserver=self.server,
                                 destroy=False,
                                 srctext=self.program,
                                 ask=q)
        
        pengine = Pengine(builder=builder, debug=False)

        # note: may be rewritten after this is fixed and pushed to pypi:
        # https://github.com/ian-andrich/PythonPengines/issues/14
        if pengine.currentQuery is not None:
            for r in pengine.currentQuery.availProofs:
                yield self._translate(r)
            pengine.currentQuery.availProofs = [] # reset
        n=0
        while pengine.currentQuery is not None and pengine.currentQuery.hasMore:
            n += 1
            logging.info(f"Next chunk={n}")
            pengine.doNext(pengine.currentQuery)
            if pengine.currentQuery is not None:
                for r in pengine.currentQuery.availProofs:
                    yield self._translate(r)
                pengine.currentQuery.availProofs = [] # reset


    def _translate(self, term):
        if type(term) == dict:
            if 'args' in term and 'functor' in term:
                if term['functor'] == 'literal':
                    return self._translate_literal(term['args'][0])
            else:
                for k,v in term.items():
                    v = self._translate(v)
                    term[k] = v
        return term

    def _translate_literal(self, v):
        if type(v) == dict:
            if v['functor'] == 'lang':
                args = v['args']
                return Literal(args[1], lang=args[0])
        else:
            return v
                
@click.command()
@click.option('-u', '--server', default=DEFAULT_SERVER, help='URL of SPARQLProg pengines server.')
@click.option('-e', '--endpoint', help='shortname of endpoint, e.g. dbpedia.')
@click.option('-p', '--program', help='prolog program to load.')
@click.option('-r', '--rule', multiple=True, help='sparqlprog rules to load.')
@click.option('-v', '--verbosity', count=True, help='verbosity')
@click.argument('query')
def sprog(server, endpoint, program, rule, verbosity, query):
    """
    Launch sparqlprog query.

    Query wikidata for continents:

        sparqlprog.py -u http://localhost:9083 -e wd "continent(X)"

    Query dbpedia for bands:

        sparqlprog.py -u http://localhost:9083 -e dbpedia "dbpedia:band(B), dbpedia:genre(B,G)"

    Example of using custom predicates; find bands that are both country and thrash metal:

        sparqlprog.py -u http://localhost:9083 -e dbpedia \
          -r "thrash_metal(Band) :- dbpedia:has_genre(Band,dbr:'Thrash_metal')" \
          -r "country_music(Band) :- dbpedia:has_genre(Band, dbr:'Country_music')" \
          "thrash_metal(B),country_music(B)"

    """
    if verbosity >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    
    logging.info(f"server={server} e={endpoint}")
    S = SPARQLProg(server=server,
                   endpoint=endpoint,
                   rules=rule,
                   program=program)
    res = S.query(query)
    n=0
    for v in res:
        n += 1
        print(f"RESULT={v}")
    logging.info(f'|Results|={n}')

if __name__ == '__main__':
    sprog()
    
        
        
    
