include("sistemas.jl")

A = [1 2 3.0; 4 5.0 6; 7.0 8 9]
b = [1.0, 2.0, 3.0]

m, v = gaussian_elimination(A, b)

print(m, v)