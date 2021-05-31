# pokeapi
Application of PokeApi services  
Expose a webservice retrieving info about a pokemon including its evolutions  
main service: */api/v1/pokemon/{name_of_pokemon}*

## Install

```
python3 -m venv .venv  # create a virtualenviroment
source .venv/bin/activate # Activate virtualenviroment
pip install -r requirements.txt # install dependencies
```

## Run server

```
python manage.py makemigrations pokeapi # create custom models
python manage.py migrate # perform actions on db
python manage.py runserver # run servers
```

## How to Use

Server consists in to expose a webservice that receive only one parameter, **pokemon name** and retrieve some info about pokemon and its evolutions
and a command line application to fetch and store data from services of pokeapi evolution_chains, command must be executed at first 
otherwise there would not be any data to consume  
webservice does not required an authentication method

### Command line Application

Command can run through manage.py as any other commmand of django framework and receive an integer o space separated integers as parameters

```
python manage.py fetchpokemondata -h  # runs built-in help
python manage.py fetchpokemondata 1  # fetch and store evolution-chain(pokeapi) with id 1
python manage.py fetchpokemondata 1 2 3  # fetch and store evolution-chains with ids 1,2,3...
```

### Web service

It requires to initialize the server, it only response in JSON format

eg. 

```
/api/v1/pokemon/pikachu
{
    "pokemon": {
        "id": 1,
        "name": "bulbasaur",
        "weight": 69,
        "height": 7,
        "base_stats": [
            {
                "base_stat": 45,
                "effort": 0,
                "name": "hp",
                "url": "https://pokeapi.co/api/v2/stat/1/"
            },
            {
                "base_stat": 49,
                "effort": 0,
                "name": "attack",
                "url": "https://pokeapi.co/api/v2/stat/2/"
            },
            {
                "base_stat": 49,
                "effort": 0,
                "name": "defense",
                "url": "https://pokeapi.co/api/v2/stat/3/"
            },
            {
                "base_stat": 65,
                "effort": 1,
                "name": "special-attack",
                "url": "https://pokeapi.co/api/v2/stat/4/"
            },
            {
                "base_stat": 65,
                "effort": 0,
                "name": "special-defense",
                "url": "https://pokeapi.co/api/v2/stat/5/"
            },
            {
                "base_stat": 45,
                "effort": 0,
                "name": "speed",
                "url": "https://pokeapi.co/api/v2/stat/6/"
            }
        ]
    },
    "evolutions": [
        {
            "id": 2,
            "name": "ivysaur",
            "type": "Evolution"
        },
        {
            "id": 3,
            "name": "venusaur",
            "type": "Evolution"
        }
    ]
}
```

There is an auxiliary service that provide a list of available pokemons to search

eg.
```
api/v1/pokemon/

{
    "available_pokemons": [
        {
            "name": "bulbasaur"
        },
        {
            "name": "charmander"
        },
        {
            "name": "squirtle"
        },
...
```

### Test

There are 7 test cases that probes correct works of services and command line applications, to run test cases do the following:

```
python manage.py test
```
