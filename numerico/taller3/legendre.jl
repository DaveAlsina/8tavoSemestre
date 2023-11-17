include("integration.jl")

using Symbolics

function legendre_polynomials(degree)
    """
        Calculates the roots of the polinomial of degree degree.
    """
    #calculate the roots of the polinomial
    @variables x
    phi = [x for i in 1:degree+2]
    phi[1] = 0 #index -1 is index 1
    phi[2] = 1 #index 0 is index 2

    for k in 0:degree-1
        fn = (2*k + 1)*x*phi[k+2] - k*phi[k+1]
        fn = fn/(k+1)

        phi[k+3] = fn
    end
    
    return phi
end

function coefs_legendre(f, polynomials, lower_limit, upper_limit; tol = 1e-8)
    """
        Calculates the coefficients of the polinomial of grade grade.
    """
    #calculate the coeficients of the polinomial
    n = length(polynomials)
    coefs = zeros(n)

    for k in 0:length(coefs)-1
        polynomial_norm = (2/(2*(k-1) + 1)) 
        poly_fn         = Symbolics.build_function(polynomials[k+1], x, expression = false)
        func            = (x) -> (f(x) * poly_fn(x))
        aj              = (1/polynomial_norm) * adaptative_integral(func, lower_limit, upper_limit, tol)
        coefs[k+1]      = aj
    end
    
    return coefs
end

function legendre(f, a, b, grade; tol = 1e-8)
    """
        Calculates the integral of a function f using the Legrende method.
    """

    #calculate the polynomials
    polynomials = legendre_polynomials(grade)
    coefs       = coefs_legendre(f, polynomials, a , b, tol = tol)
    n           = length(coefs)
    legendre_poly = 0

    print("Number of polynomials: ", length(polynomials), "\n")
    print("Coefficients: ", length(coefs), "\n")

    for i in 1:n
        legendre_poly += coefs[i] * polynomials[i]
    end
    return Symbolics.build_function(legendre_poly, x, expression = false)
end