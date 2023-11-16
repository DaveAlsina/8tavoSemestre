include("integration.jl")
using Symbolics

function roots_legendre(grade)
    """
        Calculates the roots of the polinomial of grade grade.
    """
    #calculate the roots of the polinomial
    @variables x
    phi = [ x for i in 1:grade+2]
    phi[1] = 0
    phi[2] = 1

    for k in 0:grade-1
        phi[k+3] = ((2(k)+1) * phi[k+2] * x - (k)*phi[k+1])/(k+1)
    end
    
    return phi
end

function coefs_legendre(f, roots, lower_limit, upper_limit)
    """
        Calculates the coefficients of the polinomial of grade grade.
    """
    #calculate the coeficients of the polinomial
    n = length(roots)
    coefs = zeros(n-1)

    for i in 2:n
        g = Symbolics.build_function(roots[i], x, expression = false)
        a = 1/(2/(2*i + 1)) 
        func = (x) -> (f(x) * g(x))
        aj = a * simpson_composite(func, lower_limit, upper_limit, 4)
        coefs[i-1] = aj
    end
    
    return coefs
end

function legendre(f, a, b, grade)
    """
        Calculates the integral of a function f using the Legrende method.
    """
    #calculate the roots of the polinomial
    roots = roots_legendre(grade)
    coefs = coefs_legendre(f, roots, a , b)
    n = length(coefs)
    
    p = 0

    for i in 1:n
        p += coefs[i] * roots[i+1]
    end
    return Symbolics.build_function(p, x, expression = false)
end