#from distutils.core import setup
from setuptools import setup

import sparqlprog

pt_classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

# NOTE: make release seems to be failing unless README is commented out...
setup(
    name = "sparqlprog",
    py_modules=["sparqlprog"],
    version = sparqlprog.__version__,
    description = "Execute logic program queries against a remote SPARQL endpoint",
    long_description=open("README.rst").read(),
    author = "Chris Mungall",
    author_email = "cmungall+github@gmail.com",
    url = "https://github.com/cmungall/sparqlprog-python",
    license = "BSD3",
    #tests_require = ["pytest"],
    keywords = ["prolog", "swipl", "swi-prolog", "logic programming", "pengines", "sparql", "semantic web", "owl"],
    classifiers = pt_classifiers,
)
