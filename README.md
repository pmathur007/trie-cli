# trie-cli
A CLI to interact with a global trie data structure.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install trie-cli.

```bash
pip install trie-cli
```

## Usage

The CLI includes methods to modify the global state of a trie hosted online.

Insert a keyword into the trie:
```bash
trie-cli insert [YOUR KEYWORD]
```
Delete a keyword from the trie:
```bash
trie-cli delete [YOUR KEYWORD]
```
Search for a keyword in the trie (returns True if the keyword is found/False if not):
```bash
trie-cli search [YOUR KEYWORD]
```
Return a list of autocomplete suggestions based on an input prefix
```bash
trie-cli autcomplete [YOUR PREFIX]
```
Display the trie:
```bash
trie-cli display
```
For detailed information on command format, run ```trie-cli --help```.

## Server
The trie-cli global state methods are hosted in a Flask server in Heroku. The global state is stored in a Neo4j graph database running in [Neo4j Sandbox](https://neo4j.com/sandbox/). Use the following REST endpoints to test the server.

| Name | Method | curl |
|--------------|--------|-----------------------------------------------------------------------------------------------------|
| insert | PUT | ```curl -X PUT -d keyword=[YOUR KEYWORD] "https://gentle-brushlands-20368.herokuapp.com/insert"``` |
| delete | DELETE | ```curl -X DELETE "https://gentle-brushlands-20368.herokuapp.com/delete?keyword=[YOUR KEYWORD]"``` |
| search | GET | ```curl -X GET "https://gentle-brushlands-20368.herokuapp.com/search?keyword=[YOUR KEYWORD]"``` |
| autocomplete | GET | ```curl -X GET "https://gentle-brushlands-20368.herokuapp.com/autocomplete?prefix=[YOUR PREFIX]"``` |
| display | GET | ```curl -X GET "https://gentle-brushlands-20368.herokuapp.com/display"``` |

The CLI uses the ```requests``` Python library to call the server endpoints.

## Tests
A list of commands for testing the CLI can be found in ```tests.sh```.

## Sources Consulted
CLI:
* [https://click.palletsprojects.com/en/7.x/](https://click.palletsprojects.com/en/7.x/)
* [https://docs.python-requests.org/en/master/](https://docs.python-requests.org/en/master/)

Neo4J:
* [https://py2neo.org/2021.0/index.html](https://py2neo.org/2021.0/index.html)
* [https://github.com/elena/py2neo-quickstart](https://github.com/elena/py2neo-quickstart)

Heroku:
* [https://realpython.com/flask-by-example-part-1-project-setup/](https://realpython.com/flask-by-example-part-1-project-setup/)

PyPI:
* [https://packaging.python.org/](https://packaging.python.org/)


## License
[MIT](https://choosealicense.com/licenses/mit/)