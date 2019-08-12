import os
import unittest
from prologterms import TermGenerator, PrologRenderer, Program, Var
from sparqlprog import SPARQLProg
import logging

server = 'http://localhost:9083'
P = TermGenerator()

class TestSPARQLProg(unittest.TestCase):
    """
    basic test
    """
    
    def test_basic(self):
        """ foo """

        # note: in new version of sparqlprog_wikidata, multiple 
        S = SPARQLProg(server=server,
                       endpoint='wd')
        C = Var('C')
        N = Var('N')
        query = (P.continent(C), P.enlabel(C, N))
        res = S.query(query)
        n = 0
        cs = []
        for r in res:
            n += 1
            continent = r['C']
            name = r['N']
            t = type(name)
            print(f"RESULT={continent} {name} {t}")
            cs.append(continent)
        print(f'|R|={n}')
        # check we have Africa
        self.assertTrue('http://www.wikidata.org/entity/Q15' in cs)
        self.assertTrue( n >= 8 )

if __name__ == '__main__':
    unittest.main()
