include("systems.jl")

A = [1 2 3.0; 4 5.0 6; 7.0 8.1 9]
b = [1.0, 2.0, 3.0]

m, v, x = direct_matrix_solution(A, b, type="gaussian_elimination")
println(m)
println(v)
println(x)
println()

m, v, x = direct_matrix_solution(A, b, type="partial_pivoting")
println(m)
println(v)
println(x)
println()

m, v, x = direct_matrix_solution(A, b, type="scaled_partial_pivoting")
println(m)
println(v)
println(x)
println()