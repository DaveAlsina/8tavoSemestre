include("error_metrics.jl")

function trapezoidal_approx(f::Function, x0::Float64, x1::Float64)::Float64
    """
    This function computes the trapezoidal approximation of the integral of f between x0 and x1.
    
    Input:
    ----------------
    f: Function
        The function to be integrated.
    x0: Float64
        The lower bound of the integral.
    x1: Float64
        The upper bound of the integral.

    Output:
    ----------------
    Float64
        The trapezoidal approximation of the integral of f between x0 and x1.
    """

    epsilon = x1 - x0
    return (epsilon/2)*(f(x0) + f(x1))
end


#----

function trapezoidal_composite(f::Function, x0::Float64, x1::Float64, epsilon::Float64)::Float64

    xs = [x for x in x0:epsilon:x1]

    integral = 0.0

    for i in 2:length(xs) - 1
        integral += 2*f(xs[i])
    end
    
    integral += f(x0) + f(x1)
    integral *= (epsilon/2)

    return integral
end

function trapezoidal_composite(f::Function, x0::Float64, x1::Float64, n::Integer)::Float64

    epsilon = (x1 - x0)/n
    xs = [(x0 + i*epsilon) for i in 1:1:n-1]

    integral = 0.0

    for x in xs
        integral += 2*f(x)
    end
    
    integral += f(x0) + f(x1)
    integral *= (epsilon/2)

    return integral
end

#-----------

function simpson_rule_approx(f::Function, x0::Float64, x1::Float64)::Float64
    epsilon = (x1 - x0)/2
    x2 = (x0 + x1)/2
    return (epsilon/3)*(f(x0) + 4*f(x2) + f(x1))
end


function simpson_composite(f::Function, x0::Float64, x1::Float64, epsilon::Float64)::Float64

    xs = [x for x in x0:epsilon:x1]
    n = length(xs)

    integral = 0.0

    #this does not follow the literal formula in the slides, but it is equivalent
    #it's just adapted to the way the xs are generated
    for i in 2:n-1
        if i % 2 != 0
            integral += 2*f(xs[i])
        else
            integral += 4*f(xs[i])
        end
    end
    
    integral += f(x0) + f(x1)
    integral *= (epsilon/3)

    return integral
end

function simpson_composite(f::Function, x0::Float64, x1::Float64, n::Integer)::Float64

    epsilon = (x1 - x0)/n
    xs = [(x0 + i*epsilon) for i in 1:1:n-1]

    integral = 0.0

    for i in 1:1:n-1
        if i % 2 == 0
            integral += 2*f(xs[i])
        else
            integral += 4*f(xs[i])
        end
    end
    
    integral += f(x0) + f(x1)
    integral *= (epsilon/3)

    return integral
end

#----

function simpson_fraction_rule_approx(f::Function, x0::Float64, x1::Float64)::Float64
    """
    Simpson's Fractional Rule
    """

    # 3/8 Simpson's Rule
    # using 4 points
    n = 3
    epsilon = (x1 - x0)/n

    xs = [x0 + i*epsilon for i in 0:n]
    coefficients = [1, 3, 3, 1]
    integral = 0.0

    for i in 1:length(xs)
        integral += (f(xs[i]) * coefficients[i]) * (3/8) * epsilon
    end

    return integral
end

#--------
function simpson_fraction_composite(f::Function, x0::Float64, x1::Float64, epsilon::Float64)::Float64
    """
    Simpson's Fractional Rule, Composite
    """

    xs = [x for x in x0:epsilon:x1]
    n = length(xs)

    integral = 0.0

    for i in 1:n-1
        integral += simpson_fraction_rule_approx(f, xs[i], xs[i+1])
    end

    return integral
end

function simpson_fraction_composite(f::Function, x0::Float64, x1::Float64, n::Integer)::Float64
    """
    Simpson's Fractional Rule, Composite
    """

    epsilon = (x1 - x0)/n
    xs = [(x0 + i*epsilon) for i in 0:1:n]

    integral = 0.0

    for i in 1:n
        integral += simpson_fraction_rule_approx(f, xs[i], xs[i+1])
    end

    return integral
end

#-------

function romberg_approx(f::Function, x0::Float64, x1::Float64, n::Integer)::Float64
    """
    Romberg's Method
    """

    ns = [2^i for i in 0:n]

    # first round of trapezoidal rule
    r = [trapezoidal_composite(f, x0, x1, n) for n in ns]

    # next rounds
    while length(r) >= 2 
        
        r_placeholder = zeros(length(r) - 1)
        
        for i in 1:length(r) - 1
            r_placeholder[i] = (4*r[i+1] - r[i])/3
        end
    
        r = r_placeholder
    end

    return r[1]
end

