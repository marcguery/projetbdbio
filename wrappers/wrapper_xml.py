#!/usr/bin/python3
# -*- coding: utf-8 -*-
# version 2018-01-21
# run : python wrapper_xml.py
# =============================================================================
#	Class for interacting with XML files
# =============================================================================

import xml.etree.ElementTree as ET # http://docs.python.org/3.6/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

"""
WrapperXML class for parsing and querying XML files
"""

class WrapperXML:

    def __init__(self, xml_file):
        self.xml_file = xml_file # path of the xml file
        self.tree = ET.parse(self.xml_file)

    def get_root(self):
        return self.tree.getroot()

    def query_xpath(self, xpath):
        # in etree, xpath module is quite limited, and if the XML file has a namespace, queries must use it :(
        return self.tree.findall(xpath)
    def findall(self, xpath, namespaces):
        return self.tree.findall(xpath, namespaces)

# a simple example
if (__name__ == "__main__"):
    file_tp3 = 'sources/tp3.xml'  # path to tp3 (XML)
    conn_tp3 = WrapperXML(file_tp3)
    	
