# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from _mapping import entities
 
elastic = Elasticsearch(hosts=["elastic"])
