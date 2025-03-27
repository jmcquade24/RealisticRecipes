from algoliasearch.search.client import SearchClient
import os

# Sets up proxy, because pythonanywhere doesn't let me access algolia directly
os.environ["HTTPS_PROXY"] = "http://proxy.server:3128"
os.environ["HTTP_PROXY"] = "http://proxy.server:3128"

# Initialize the Algolia client
client = SearchClient("6RFFC8176O", "2c5f07a0be0b6a6f7ddfaaa263ad6474")