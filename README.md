# foodweb prediction

A study about how to calculate interactions between variables from timeseries.

## About

Theoretically it is possible to assess interactions between variables from timeseries data.
The interaction strengths express how much the changes of a variable influences changes in another
(partial derivatives). Due to the simulateneous changes of N number of variables these partial derivatives
can only be calculated from the same number of temporal datapoints.
From a sample of datapoints the partial derivatives can be estimated by calculating an appropriate linear combination of the directional changes. Using many samples the estimation can be made more precise.

In the present biological example the interacting variables are population sizes of different species.
These species are members of a food web, where each predator pray link means a positive and a negative interaction
between the two species respectively (the partial derivative of the growth rate of a species with respect to the population size of another one). Notice that in this case the sign of the interactions is independent of the population sizes.
Using the above described method we can try to predict the a food web (a set of predator-prey interactions) species from population size timeseries of the consituting species.

## Software / libraries
- Python
- numpy, matplotlib, graphviz

## How to use

Run by 'python foodweb.py' with the other sources files in the same folder. Results will be saved into
a 'sim' subdirectory.

## Results
Python, pyTorch, pyOpenGL
