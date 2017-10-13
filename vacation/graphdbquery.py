# -*- coding: utf-8 -*-

from neo4j.v1 import GraphDatabase, basic_auth


class Neo4jDriver(object):

    def __init__(self, address, port, name, password):
        self.driver = GraphDatabase.driver("bolt://{0}:{1}".format(address, port), 
                auth=basic_auth(name, password))
        self.session = self.driver.session()

    def query(self, **kwargs):
        pass
