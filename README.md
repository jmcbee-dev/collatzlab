# collatzlab
Library for Collatz iterative functions

Work in progress

# Features
The primary features of this library is the ability to disect a parity vector and obtain the set of numbers satisfying the associated diophantine equation.

For example, the parity vector `10100100` is described by the diophantine equation 2^5 y - 3^3 x = 23, which has an infinite set of integer solutions.
One particular solution is x = 11, y = 10, which can be found by solving the diophantine equation using the extended euclidian algorithm, then taking the modulous of the general solution to x (mod 2^5), to get 11.

The result is 11 follows the parity vector described above, where `1` represents an odd number, `0` an even number. This can be used as a tool to finding seive starting points if needed.
