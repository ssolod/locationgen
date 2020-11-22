# Random Location Generator within a Country

## Goals
* Implement a helper script to generate a given number of random points within a
boundary of a country.
* Accomodate a random generator and 'skewed' generation toward the large cities.

## How to use
Run for usage:
```
./generate.py -h
```

The following modes are currently supported:
| Mode   | Description                                           | Requires                                             |
|--------|-------------------------------------------------------|------------------------------------------------------|
| RANDOM | Generates a random set of points within a country.    | Country boundary CSV file.                           |
| URBAN  | Generates a random set of points around large cities. | Country boundary CSV file. Cities metadata CSV file. |
| MIXED  | RANDOM and URBAN methods are used 50/50.              | Country boundary CSV file. Cities metadata CSV file. |

## Examples
### Generate a set of random points (RANDOM mode)
```
./generate.py -n 10 -f by.csv -m random
```

### Generate a set of random points around large cities (URBAN mode)
```
./generate.py -n 10 -f by.csv -c bycities.csv -m urban 
```

### Generate a set of random points around large cities and additionally everywhere in the country (MIXED mode)
```
./generate.py -n 10 -f by.csv -c bycities.csv -m mixed 
```


