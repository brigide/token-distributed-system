# Python token generator 

Python token generator based on distributed python processes connected via sockets.

# How to run

First, it's essential to install the used dependencys using any python environment:
  - scipy
  - matplotlib
  - sympy
  - numpy

Then, you can run both processes using p1.py (evaluation of the inputs) and p2.py (actual token generator) and use client.py to call the evaluation process.

In both processes, there are some argument options such as port (-p/--port) and host(-H/--host) (e.g. python p1.py -H 192.168.0.1 -p 50002).

# Testing

There is a testing script (test.py) that can run and generate multiple tokens based on iterations and seconds to benchmark it's performance.

There are also some options to run different tests.
  - number of iterations: -i or --iterations
  - number of seconds: -s or --seconds

# Result example

image here

results
iteration: 1
token count: 30
average tokens per second: 6.0
avarage time to generate: 0.18s

iteration: 2
token count: 30
average tokens per second: 6.0
avarage time to generate: 0.15s

iteration: 3
token count: 30
avarage time to generate: 0.14s

iteration: 4
token count: 29
average tokens per second: 5.8
avarage time to generate: 0.20s

iteration: 5
token count: 29
average tokens per second: 5.8
avarage time to generate: 0.17s

mean:  29.6
variance:  1.2
standard deviation:  0.24
