# termooo-solver

This repository helds a simple python project meant to help solve `term.ooo` game.

## How it works?

`5_chars_words.txt` is a database of all Portuguese words of 5 characters.

The program iterate through this database, applying the necessary filters based on the options passed.

## What are the options?

_Obs: All options can be used together._

### `-e`

The excluded characters option.<br/>
You pass all the characters (comma separated) that the solution do not have. Ex:

`python main.py -e a,b,c`

### `-i`

The included characters option.<br/>
You pass all the characters (comma separated, in the format `character-position`) that the solution have, but you dont know the exact position. Ex:

`python main.py -i g-1,e-4`

### `-x`

The included characters option, in the exact position. You pass all the characters (comma separated, in the format `position-character`) that the solution have, but you know the exact position. Ex:

`python main.py -x g-1,e-4`

## Prerequisites

* Python 3.6+

## Authors

* **Flavio Teixeira** - *Initial work* - [ap3xx](https://github.com/ap3xx)

