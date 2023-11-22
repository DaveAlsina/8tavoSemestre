using Symbolics
include("integration.jl")

function fourier_coefficients(fn, n, T, tol=1e-6; lower_lim = nothing, upper_lim = nothing)
    
    """
        Calculate the Fourier coefficients of the function fn.

        Input:
        --------------
            fn: Function to calculate the Fourier coefficients.
            n: Number of coefficients to calculate.
            T: Period of the function.
            tol: Tolerance for the Simpson's rule.
            lower_lim: Lower limit of the integral.
            upper_lim: Upper limit of the integral.

        Output:
        --------------
            a_0: Fourier coefficient a_0.
            a_k: Vector of Fourier coefficients a_k.
            b_k: Vector of Fourier coefficients b_k.
    """

    L = T / 2
    ω = 2π / T

    if isnothing(lower_lim)
        lower_lim = -L
    end

    if isnothing(upper_lim)
        upper_lim = L
    end

    a_0 =  (1 / L) * simpson_fraction_composite(x -> fn(x),              lower_lim, upper_lim, tol)
    a_k = [(1 / L) * simpson_fraction_composite(x -> fn(x) * cos(k*ω*x), lower_lim, upper_lim, tol) for k in 1:n]
    b_k = [(1 / L) * simpson_fraction_composite(x -> fn(x) * sin(k*ω*x), lower_lim, upper_lim, tol) for k in 1:n]
    return a_0, a_k, b_k
end

function partial_sum(a_0, a_k, b_k, n, T)
    """
        Calculate the partial sum of the Fourier series.

        Input:
        --------------
            a_0: Fourier coefficient a_0.
            a_k: Vector of Fourier coefficients a_k.
            b_k: Vector of Fourier coefficients b_k.
            n: Number of coefficients to calculate.
            T: Period of the function.

        Output:
        --------------
            sum_val: Partial sum of the Fourier series.
    """
    @variables x
    sum_val = a_0 / 2

    ω = 2π / T

    for k in 1:n
        sum_val += a_k[k] * cos(k*ω*x) + b_k[k] * sin(k*ω*x)
    end

    return Symbolics.build_function(sum_val, x, expression = false)
end

function fourier(fn::Function, T, n, tol=1e-6; lower_lim = nothing, upper_lim = nothing)

    """
        Calculate the Fourier series of the function fn.

        Input:
        --------------
            fn: Function to calculate the Fourier series.
            T: Period of the function.
            n: Number of coefficients to calculate.
            tol: Tolerance for the Simpson's rule.
            lower_lim: Lower limit of the integral.
            upper_lim: Upper limit of the integral.

        Output:
        --------------
            sum_val: Partial sum of the Fourier series.
    """

    a_0, a_k, b_k = fourier_coefficients(fn, n, T, tol, lower_lim = lower_lim, upper_lim = upper_lim)
    return partial_sum(a_0, a_k, b_k, n, T)
end

#------------------------------------------------------------
#             Discrete trigonometric aproximation
#------------------------------------------------------------

function discrete_trigonometric_coefficients(xj, yj, nterms, T)

    ak = []
    ω = 2π / T

    for k in 0:nterms
        sum_val = sum([yj[j]*cos(k*xj[j]*ω) for j in 1:length(xj)])
        sum_val *= 1/(length(xj)//2)
        push!(ak, sum_val)
    end

    bk = []

    for k in 1:nterms-1
        sum_val = sum([yj[j]*sin(k*xj[j]*ω) for j in 1:length(xj)])
        sum_val *= 1/(length(xj)//2)
        push!(bk, sum_val)
    end

    return ak, bk
end

function discrete_trigonometric_approx(points, nterms, T)

    points_ = deepcopy(points)

    xj = [p[1] for p in points]
    yj = [p[2] for p in points]
    ω  = 2π / T

    ak, bk = discrete_trigonometric_coefficients(xj, yj, nterms, T)

    @variables x
    sum_val = ak[1]/2
    sum_val += ak[end]*cos(nterms*x)

    for k in 1:nterms-1
        sum_val += ak[k+1]*cos(k*x*ω) + bk[k]*sin(k*x*ω)
    end

    return Symbolics.build_function(sum_val, x, expression = false)
end