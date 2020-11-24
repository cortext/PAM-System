# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from _mapping import entities

elastic = Elasticsearch(
            http_auth=("", ""),
            scheme="http",
            port=9200,
          )

# make an API call to the Elasticsearch cluster
# and have it return a response:
response = elastic.indices.create(
    index="entities",
    body=entities,
    ignore=400  # ignore 400 already exists code
)


if 'acknowledged' in response:
    if response['acknowledged'] is True:
        print("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
elif 'error' in response:
    print("ERROR:", response['error']['root_cause'])
    print("TYPE:", response['error']['type'])
