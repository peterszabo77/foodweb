# foodweb
Calculating interactions from timeseries in a biological context.

A study about how to calculate interactions between variables from timeseries.

## About

Theoretically it is possible to assess interactions between interacting variables from timeseries data.
These interaction strengths express how much the changes of a variable influences changes in another
(partial derivatives). Due to the simulateneous changes of variables in the timeseries these partial derivatives
can only be calculated from samples of N datapoints, where N is the number of interacting variables.
Within a sample the partial derivatives can be estimated by using a linear combination of the directional changes.
Using many samples the estiamtion can be made more precise.
In the present biological example the interacting variables are population sizes of different species.
These species are members of a food web, where each predator pray link means a positive and a negative interaction
between the two species respectively. Notice that in this case the sign of the interactions
is independent of the population sizes.
Using the above described method we can try to predict the food web (predator-prey interactions) among several
species from the timeseries of their population sizes.

## Software / libraries
- Python
- numpy, matplotlib, graphviz

## Results
Python, pyTorch, pyOpenGL
