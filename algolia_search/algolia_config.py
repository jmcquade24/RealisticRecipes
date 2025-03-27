import algoliasearch.http
from algoliasearch.search.client import SearchClient
from algoliasearch.search import config
import algoliasearch
import requests
import os
	
from algoliasearch.http.hosts import Host, HostsCollection
from algoliasearch.search.config import SearchConfig

import requests.adapters

# Sets up proxy, because pythonanywhere doesn't let me access algolia directly
config = SearchConfig (
    app_id="6RFFC8176O",
    api_key="2c5f07a0be0b6a6f7ddfaaa263ad6474",
)

client = SearchClient(config=config)
