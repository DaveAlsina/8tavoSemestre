
#------------------------------------------------------------
#        Functions to evaluate the regression functions
#------------------------------------------------------------

function standard_stimation_error(points::Vector, fn::Function)
    """
        Retrieve the data dispersion of the sample around the regression function.

        Input:
        --------------
            points: Vector of tuples (x, y) representing the points
            of the sample.
            fn: Function representing the regression function.

        Output:
        --------------
            syx: Standard stimation error.
    """
    sr = sum([(p[2] - fn(p[1]))^2 for p in points])
    syx = sqrt(sr/(length(points) - 2))

    return syx
end


#------------------------------------------------------------
#         Functions to calculate the regression coefficients
#------------------------------------------------------------

function linear_regression(points:: Vector)
    """
        Input:
        --------
            points: Vector of tuples (x, y) representing the points
            of the sample.

        Output:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.
    """

    n = length(points)

    sumx = sum([p[1] for p in points])
    sumy = sum([p[2] for p in points])
    sumxy = sum([p[1]*p[2] for p in points])
    sumx2 = sum([p[1]^2 for p in points])

    ymean = sumy/n
    xmean = sumx/n

    a1 = (n*sumxy - sumx*sumy)/(n*sumx2 - sumx^2)
    a0 = ymean - a1*xmean

    return (a0, a1)
end

function exp_regression(points::Vector)

    """
        Linearize the exponential regression and then apply linear regression.

        Input:
        --------
            points: Vector of tuples (x, y) representing the points
            of the sample.

        Output:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.
    """

    points = deepcopy(points)
    points = [(p[1], log(p[2])) for p in points]
    (a0, a1) = linear_regression(points)

    return (exp(a0), a1)
end

function power_regression(points::Vector)

    """
        Linearize the power regression and then apply linear regression.

        Input:
        --------
            points: Vector of tuples (x, y) representing the points
            of the sample.
        
        Output:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.
    """

    points = deepcopy(points)
    points = [(log(p[1]), log(p[2])) for p in points]
    (a0, a1) = linear_regression(points)

    return (exp(a0), a1)
end

function growth_rate_regression(points::Vector)

    """
        Linearize the growth rate regression and then apply linear regression.

        Input:
        --------
            points: Vector of tuples (x, y) representing the points
            of the sample.
        
        Output:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.
    """

    points = deepcopy(points)
    points = [(1/p[1], 1/p[2]) for p in points]

    (a0, a1) = linear_regression(points)

    return (1/a0, a1/a0)
end


#------------------------------------------------------------
#     Functions to calculate the polynomial regression
#------------------------------------------------------------

function polynomial_regression(points::Vector, nvars::Integer)
    
    mat = zeros(nvars, nvars)

    # Fill the matrix
    for i in 1:nvars
        for j in 1:nvars
            mat[i, j] = sum([p[1]^(i+j-2) for p in points])
        end
    end

    # Fill the vector
    vec = zeros(nvars)

    for i in 1:nvars
        vec[i] = sum([ (p[1]^(i-1))*p[2] for p in points ])
    end

    # Solve the system
    a = mat\vec

    return a
end



#------------------------------------------------------------
#         Functions to build the regression functions
#------------------------------------------------------------

function build_lin_fn(a0::Float64, a1::Float64)
    """
        Input:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.

        Output:
        --------
            fn: Function representing the linear regression.
    """

    fn = (x) -> a0 + a1*x
    return fn
end

function build_exp_fn(a0::Float64, a1::Float64)
    """
        Input:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.

        Output:
        --------
            fn: Function representing the exponential regression.
    """
    fn = (x) -> a0*exp(a1*x)
    return fn
end

function build_pow_fn(a0::Float64, a1::Float64)

    """
        Input:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.

        Output:
        --------
            fn: Function representing the power regression.
    """

    fn = (x) -> a0*(x^a1)
    return fn
end

function build_growth_rate_fn(a0::Float64, a1::Float64)

    """
        Input:
        --------
            a0: Intercept of the linear regression.
            a1: Slope of the linear regression.

        Output:
        --------
            fn: Function representing the growth rate regression.
    """

    fn = (x) -> a0*(x/(a1 + x))
    return fn
end

function build_poly_fn(a::Vector)
    """
        Input:
        --------
            a: Vector of coefficients of the polynomial regression.

        Output:
        --------
            fn: Function representing the polynomial regression.
    """

    fn = (x) -> sum([a[i]*x^(i-1) for i in 1:length(a)])
    return fn
end