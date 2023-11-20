include("integration.jl")
using Symbolics

#---------------------------------------------#
#           Legendre continuous               #
#---------------------------------------------#

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

function coefs_legendre(f::Function, polynomials, lower_limit, upper_limit; tol = 1e-8)
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

function legendre(f, a, b, degree; tol = 1e-8)
    """
    """

    #calculate the polynomials
    polynomials = legendre_polynomials(degree)
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

#---------------------------------------------#
#             Legendre discrete               #
#---------------------------------------------#

function coefs_legendre(points::Vector, polynomials)

    """
        Calculates the coefficients of the polinomial of degree degree.
    """
    #calculate the coeficients of the polinomial
    n = length(polynomials)
    coefs = zeros(n)
    xs = [points[i][1] for i in 1:length(points)]
    ys = [points[i][2] for i in 1:length(points)]

    #calculate the x deltas and the xs and ys averages
    #this is used in order to make better the approximation
    #of the values for the integral
    xdeltas = [xs[i+1] - xs[i] for i in 1:length(xs)-1]
    yavgs   = [(ys[i+1] + ys[i])/2 for i in 1:length(ys)-1]
    xavgs   = [(xs[i+1] + xs[i])/2 for i in 1:length(xs)-1]


    for k in 0:length(coefs)-1
        polynomial_norm = (2/(2*(k-1) + 1)) 
        poly_fn         = Symbolics.build_function(polynomials[k+1], x, expression = false)

        #calculate the integral 
        integration_fn  = (i) -> yavgs[i] * poly_fn(xavgs[i]) * xdeltas[i]
        integral_       = sum([ integration_fn(i) for i in 1:length(xs)-1])
        
        #calculate the coeficient
        aj              = (1/polynomial_norm) * integral_
        coefs[k+1]      = aj
    end
    
    return coefs

end

function legendre_discrete(points, degree)

    #calculate the polynomials
    polynomials = legendre_polynomials(degree)
    coefs       = coefs_legendre(points, polynomials)
    n           = length(coefs)

    legendre_poly = 0
    for i in 1:n
        legendre_poly += coefs[i] * polynomials[i]
    end

    return Symbolics.build_function(legendre_poly, x, expression = false)
end

