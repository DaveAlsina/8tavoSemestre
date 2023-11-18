using Symbolics
include("integration.jl")

function fourier_coefficients(fn, n, T, tol=1e-6)
    L = T / 2
    ω = 2π / T

    a_0 =  (1 / L) * simpson_fraction_composite(x -> fn(x),              -L, L, tol)
    a_k = [(1 / L) * simpson_fraction_composite(x -> fn(x) * cos(k*ω*x), -L, L, tol) for k in 1:n]
    b_k = [(1 / L) * simpson_fraction_composite(x -> fn(x) * sin(k*ω*x), -L, L, tol) for k in 1:n]
    return a_0, a_k, b_k
end

function partial_sum(a_0, a_k, b_k, n, T)
    @variables x
    sum_val = a_0 / 2

    ω = 2π / T

    for k in 1:n
        sum_val += a_k[k] * cos(k*ω*x) + b_k[k] * sin(k*ω*x)
    end

    return Symbolics.build_function(sum_val, x, expression = false)
end

function fourier(fn::Function, T, n, tol=1e-6)
    L = T / 2
    a_0, a_k, b_k = fourier_coefficients(fn, n, T, tol)

    return partial_sum(a_0, a_k, b_k, n, T)
end
