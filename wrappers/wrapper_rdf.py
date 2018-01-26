#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2018-01-22
# run : python wrapper_rdf.py
# =============================================================================
#	Class for interacting with RDF files
# =============================================================================

from rdflib import Graph # https://rdflib.readthedocs.io/en/latest/
import pprint

"""
WrapperRDF class for parsing and querying RDF data
"""

class WrapperRDF:

    def __init__(self, file_rdf, format_rdf) :
        self.triples = Graph()
        self.triples.parse(file_rdf, format=format_rdf)

    def get_graph_size(self) :
        if self.triples :
            return len(self.triples)
        return 0

    def query_sparql(self, query) :
        res = self.triples.query(query)
        return res

    def print_graph(self):
        if self.triples :
            for stmt in self.triples :
                pprint.pprint(stmt)

# a simple example
if (__name__ == "__main__"):
    file_tp4 = 'sources/tp4.ttl'  # path to tp4 (RDF)
    format_file_tp4 = 'n3'  # format of the RDF data from tp4
    conn_rdf = WrapperRDF(file_tp4, format_file_tp4) # parsing file_tp4 takes ~30 seconds
    conn_rdf.print_graph()