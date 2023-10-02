
#---------------------------------------------------------------------------#
#                           Lagrange interpolation                          #
#---------------------------------------------------------------------------#

function lagrange_coefficients(xvalue::Float64, x::Vector, k::Int)::Float64

    """
        Calculates the lagrange coefficients for the lagrange polynomial interpolation.

        Parameters
        ----------
            xvalue: point to interpolate.
            x: list of points [x, y] to interpolate.
            k: index of the point to interpolate.
        
        Returns
        -------
            y: interpolated value.
    """

    n = length(x)
    numerator = 1
    denominator = 1

    for j = 1:n
        if j != k
            numerator = numerator * (xvalue - x[j])
            denominator = denominator * (x[k] - x[j])
        end
    end

    return numerator / denominator
end

function lagrange_polynomial(points::Vector{Vector{Float64}}, x::Float64)
    """
        Polynomial Interpolation, with lagrange polynomials.

        Parameters
        ----------
            points: list of points [x, y] to interpolate.
            x: point to interpolate.
        
        Returns
        -------
            y: interpolated value.
    """

    y = 0.0
    xpoints = [points[i][1] for i in 1:length(points)]
    ypoints = [points[i][2] for i in 1:length(points)]

    for k in 1:length(points)
        pointx = xpoints[k]
        pointy = ypoints[k]

        y += pointy * lagrange_coefficients(x, xpoints, k)
    end

    return y 
end

function divide_into_groups(x_values::Vector{Float64}, y_values::Vector{Float64})

    """
        Given a set of points, this function divides the points in three groups, the first group contains the first three points,
        the second group contains the points from the fourth to the last three points, and the third group contains the last three points.

        Arguments:
        ----------------
            x_values: Vector of x values of the points to be interpolated.
            y_values: Vector of y values of the points to be interpolated.
        
        Returns:
        ----------------
            left: Vector of points [x,y] to be interpolated.
            mid: Vector of points [x,y] to be interpolated.
            right: Vector of points [x,y] to be interpolated.
    """

    # condition (n -4) % 3 == 1  or len(x) != len(y) or len(x) < 5
    #if (length(x_values) - 4) % 3 != 1 || length(x_values) != length(y_values) || length(x_values) < 5
    #    println("The number of points is not correct")
    #    return nothing
    #end

    #ends polynomials
    left = [[x_values[i], y_values[i]] for i in 1:3]
    right = [[x_values[i], y_values[i]] for i in length(x_values)-2:length(x_values)]

    #middle polynomials, gives all the pairs of 3 points for cubic interpolation in the middle
    mid = [[ [x_values[j], y_values[j]] for j in i:i+3 ] for i in 3:3:length(x_values)-3]

    return left, mid, right
end

function find_polynomium(left::Vector{Vector{Float64}},
                         mid::Vector{Vector{Vector{Float64}}},
                         right::Vector{Vector{Float64}},
                         target::Float64)


    """
        Given a set of points, this function finds the polynomium that interpolates the points where the target is located.

        Arguments:
        ----------------
            left: Vector of points [x,y] to be interpolated.
            mid: Vector of points [x,y] to be interpolated.
            right: Vector of points [x,y] to be interpolated.
            target: value to interpolate
        
        Returns:
        ----------------
            polynomium: Vector of polynomials for the cubic spline method.
    """

    xleft = [left[i][1] for i in 1:length(left)]
    xright = [right[i][1] for i in 1:length(right)]
    xmiddles = [[mid[i][j][1] for j in 1:length(mid[i])] for i in 1:length(mid)]

    #if the targetx is between some of the left ones then return left
    if  (target <= xleft[end]) && (target >= xleft[1])
        return left

    #if the targetx is between some of the right ones then return right
    elseif (target <= xright[end]) && (target >= xright[1])
        return right

    #otherwise check if the target is between some of the middle ones
    else 
        for i in 1:length(xmiddles)
            if (target <= xmiddles[i][end]) && (target >= xmiddles[i][1])
                return mid[i]
            end
        end
    end

    error("The target x: $(target) is not between the points")
end


function plot_polynomiun(x_values::Vector{Float64}, y_values::Vector{Float64}, step::Float64)

    """
        Given a set of points, this function plots the polynomium that interpolates the points.

        Arguments:
        ----------------
            x_values: Vector of x values of the points to be interpolated.
            y_values: Vector of y values of the points to be interpolated.
            step: step to plot the polynomials
        
        Returns:
        ----------------
            polynomials: Vector of polynomials for the cubic spline method.
    """
    
    n = length(x_values)
    start = x_values[1]
    stop = x_values[end]

    #divide the set of points into groups used for the cubic interpolation
    #or quadratic with lagrange polys
    left, mid, right = divide_into_groups(x_values, y_values)

    pts = [[x, lagrange_polynomial( find_polynomium(left,mid, right, x) , x)] for x = start:step:stop]

    x = [p[1] for p in pts]
    y = [p[2] for p in pts]

    # Graficar puntos utilizando scatter() 
    plot(x, y, legend=true, title="Gráfico de Puntos", xlabel="Eje X", ylabel="Eje Y")
    # Agregar puntos de construccion
    scatter!([i for i in x_values],[i for i in y_values], label="Puntos", color=:red)   
end

function interpolate_point(samples::Vector{Vector{Float64}}, x::Float64)

    """
        Given a set of points, this function interpolates a point using the lagrange polynomials.

        Arguments:
        ----------------
            samples: Vector of points [x,y] to be interpolated.
            x: point to interpolate
        
        Returns:
        ----------------
            y: interpolated value.
    """

    #divide the set of points into groups used for the cubic interpolation
    #or quadratic with lagrange polys
    left, mid, right = divide_into_groups([s[1] for s in samples], [s[2] for s in samples])

    #find the set of points that interpolates the point
    polynomium = find_polynomium(left, mid, right, x)

    #interpolate the point
    return lagrange_polynomial(polynomium, x)
end


#---------------------------------------------------------------------------#
#                        Cubic Splines interpolation                        #
#---------------------------------------------------------------------------#

function build_continuity_coefficients(X, points)

    """10 de noviembre a partir de las 8 am.
        Given a matrix full of zeros, and of size (4n, 4n), where n is the number of polynomials to be found
        for the cubic spline, this function fills the upper part of the matrix corresponding to the equations 
        that say that the polynomials must be continuous at the intersections of the intervals.

        Arguments:
            X: Matrix of zeros of size (4n, 4n)
            points: Vector of points [x,y] to be interpolated
    """

    # Check that the matrix is square
    size(X, 1) == size(X, 2) || error("The matrix must be square")

    row = 1
    n_intervals = length(points) - 1

    # Fill the upper part of the matrix
    for i in 1:n_intervals
        
        # Columns to be filled
        cols = (4 * i - 3):(4 * i)
        
        # Points to get the coefficients to fill the columns with
        start_point = points[i]
        end_point = points[i + 1]

        X[row, cols] = [start_point[1]^3, start_point[1]^2, start_point[1], 1]
        X[row+1, cols] = [end_point[1]^3, end_point[1]^2, end_point[1], 1]
        row += 2
    end
    

    return X
end

function build_first_derivative_continuity_coefficients(X, points)

    """
        Given a matrix full of zeros, and of size (4n, 4n), where n is the number of polynomials to be found
        for the cubic spline, this function fills the middle part of the matrix corresponding to the equations 
        that say that the first derivative of the polynomials must be continuous at the intersections of the intervals, 
        this is that the first derivative of the polynomial at the end of an interval must be equal to the first derivative
        of the polynomial at the beginning of the next interval.

        Arguments:
            X: Matrix of zeros of size (4n, 4n)
            points: Vector of points [x,y] to be interpolated
    """

    # Check that the matrix is square
    size(X, 1) == size(X, 2) || error("The matrix must be square")

    n_intervals = length(points) - 1
    row = 2*(n_intervals)+ 1  # 2(n -1) + 1 

    # Fill the first mid part part of the matrix
    for i in 1:n_intervals-1
        
        # Columns to be filled
        col1 = (4 * i - 3):(4 * i)
        col2 = (4 * i + 1):(4 * i + 4)

        # Points to get the coefficients to fill the columns with
        start_point = points[i+1]

        X[row, col1] = [-3*start_point[1]^2, -2*start_point[1], -1, 0]
        X[row, col2] = [ 3*start_point[1]^2,    2*start_point[1],    1, 0]

        row += 1
    end
    
    return X
end

function build_second_derivative_continuity_coefficients(X, points)

    # Check that the matrix is square
    size(X, 1) == size(X, 2) || error("The matrix must be square")

    n_intervals = length(points) - 1
    row = 3*(n_intervals) # 3(n-1) = 3(n) -4 +1

    # Fill the second mid part part of the matrix
    for i in 1:n_intervals-1
        
        # Columns to be filled
        col1 = (4 * i - 3):(4 * i)
        col2 = (4 * i + 1):(4 * i + 4)

        # Points to get the coefficients to fill the columns with
        start_point = points[i+1]

        X[row, col1] = [-6*start_point[1], -2, 0, 0]
        X[row, col2] = [ 6*start_point[1],  2, 0, 0]

        row += 1
    end
    
    return X

end

function build_second_derivative_natural_coefficients(X, points)

    # Check that the matrix is square
    size(X, 1) == size(X, 2) || error("The matrix must be square")

    n_intervals = length(points) - 1
    row = 2*(2*(n_intervals+1)-3) + 1  # 2(2(n)-3) + 1

    # Columns to be filled
    col1 = 1:4
    col2 = (n_intervals*4 - 3):(n_intervals*4)

    # Points to get the coefficients to fill the columns with
    start_point = points[1]
    end_point = points[end]

    # Fill the second mid part part of the matrix
    X[row, col1] = [6*start_point[1], 2, 0, 0]
    X[row+1,col2] = [6*end_point[1], 2, 0, 0]

    return X
end

function build_matrix(points)
    n_intervals = length(points) - 1

    #matrix of zeros of size (4n, 4n)
    X = zeros(4 * n_intervals, 4 * n_intervals)

    #fill the upper part of the matrix and print the complete matrix
    X = build_continuity_coefficients(X, points)
    X = build_first_derivative_continuity_coefficients(X, points)
    X = build_second_derivative_continuity_coefficients(X, points)
    X = build_second_derivative_natural_coefficients(X, points)

    return X
end

function build_vector(points)

    n_intervals = length(points) - 1

    #vector of zeros of size (4n, 1)
    Y = zeros(4 * n_intervals, 1)


    #fill the upper part of the matrix and print the complete matrix
    Y[1] = points[1][2]
    Y[2*(n_intervals-1)+2] = points[end][2]

    row = 2
    for i in 2:n_intervals
        Y[row] = points[i][2]
        Y[row+1] = points[i][2]
        row += 2
    end

    return Y

end

function build_and_solve_coefficients(points)
    X = build_matrix(points)
    Y = build_vector(points)
    return X\Y
end

function build_cubic_splines(points, x)

    #sort points by x value 
    points = sort(points, by = x -> x[1])
    
    #build and solve the coefficients
    coefficients = build_and_solve_coefficients(points)
    n_intervals = length(points) - 1
    polynomials = []

    #build the polynomials
    for i in 1:n_intervals
        start_point = points[i]
        end_point = points[i+1]
        polynomial = coefficients[4*i-3]*x^3 + coefficients[4*i-2]*x^2 + coefficients[4*i-1]*x + coefficients[4*i]
        push!(polynomials, (Symbolics.build_function(polynomial, x, expression = false) , start_point[1],end_point[1]))
    end
    return polynomials
end

function interpolate(polynomals, x)
    for polynomial in polynomals
        if x >= polynomial[2] && x <= polynomial[3]
            return polynomial[1](x)
        end
    end
    return nothing
end
