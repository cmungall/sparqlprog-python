import os
import unittest
from prologterms import TermGenerator, PrologRenderer, Program, Var, Term
from sparqlprog import SPARQLProg
import logging

logging.basicConfig(level=logging.INFO)

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

    def test_program(self):
        """ foo """

        X = Var('X')
        Y = Var('Y')
        Z = Var('Z')
    
        rules = [
            P.ever_in_band(X,Y) <= P.rdf(Y, 'http://dbpedia.org/ontology/bandMember', X),
            P.ever_in_band(X,Y) <= P.rdf(Y, 'http://dbpedia.org/ontology/formerBandMember', X),
            P.has_shared_band_member(X,Y,Z) <= (P.ever_in_band(Z, X), P.ever_in_band(Z,Y))
            #P.has_shared_band_member(X,Y,Z) <= (P.ever_in_band(Z, X), P.ever_in_band(Z,Y), Term('\=', X, Y))
        ]        
        S = SPARQLProg(server=server,
                       rules=rules,
                       endpoint='dbpedia')
        metallica = 'http://dbpedia.org/resource/Metallica'
        query = (P.ever_in_band(Z,metallica), P.has_shared_band_member(X,Y,Z))
        res = S.query(query, [X,Y,Z])
        for r in res:
            print(f"RESULT={r}")

if __name__ == '__main__':
    unittest.main()
