# Town-Evolution

This project simulates the evolution of an initial population of `m` men and `f` women during a period of `p` weeks. The time flow is simulated by a uniform random variable `u ~ U (0, l)` or by a homogeneous Poisson process with the parameter `L` (these letters coincide with the parameters that must be given to the program before the execution) This simulation includes the death, engagement, breakups and pregnancies of people.

## Starting 🚀

To use the project, clone it or download it to your local computer.

### Requirements 📋

It is necessary to have python v-3.7.2

### Installation 🔧

To execute the project, there is a required param: the random variable used to simulate flow of time. To simulate it with a uniform just open the console from the root location of the project and execute:

```
python simulation.py -u
```

To simulate it with a poisson process:

```
python simulation.py -P
```

Recommended params for the poisson process:

|         Lambda          |  1  | 0.5 | 0.25 | 0.125 | 0.048 | 0.0265 |
| :---------------------: | :-: | :-: | :--: | :---: | :---: | :----: |
| Expected value of weeks |  1  |  2  |  4   |   8   |  24   |   48   |

To see a description of all possible params execute `python simulation.py -h`

To see a summary of the events occured in every turn, execute the project with the `-s` flag. This summary includes groups of people by sex and range of ages, number of women pregnats and number of people alive.

## Autores ✒️

- **Miguel Tenorio** - [stdevAntiD2ta](https://github.com/stdevAntiD2ta)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto.

## Licencia 📄

This project is under the License (MIT License) - see the file [LICENSE.md](LICENSE.md) for details.
