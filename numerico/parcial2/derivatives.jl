
#---------------------------------------------------------------------------#
#                           Common derivative                               #
#---------------------------------------------------------------------------#
function derivate(f, x, h)
    return( (f(x+h) - f(x) )/h ) 
end

#---------------------------------------------------------------------------#
#                           Three points derivatives                        #
#                               with middle point                           #
#---------------------------------------------------------------------------#

function three_point_numeric_diff_middle(f, x, h)
    """
        Three point numeric differenciation using the middle given a function f,
        a point x and an h.

        Parameters
        ----------
        f : Function
            Function to be evaluated.
        x : Float64
            Point to be evaluated.
        h : Float64
            h to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using h.
    """
    xs = [x+h, x-h]
    coefficients = [1, -1]
    denominator = 2*h

    return sum([cx[1]*f(cx[2]) for cx  in zip(coefficients, xs)])/denominator
end

function three_point_numeric_diff_middle(points::Array{Float64, 1}, epsilon::Float64)::Float64
    """
        Three point numeric differenciation using the middle point given a set of points [[x, y], ...]
        and an epsilon.

        Parameters
        ----------
        points : Array{Float64, 1}
            Set of points to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """
    if length(points) != 3
        error("The length of the points array must be 3")
    end

    coefficients = [1, -1]
    ys = [points[1][2], points[2][2]]
    denominator = 2*epsilon

    return sum([cx[1]*cx[2] for cx  in zip(coefficients, ys)])/denominator
end

#---------------------------------------------------------------------------#
#                           Three points derivatives                        #
#                             with extreme points                           #
#---------------------------------------------------------------------------#

function three_point_numeric_diff_extremes(f::Function, x::Float64, epsilon::Float64, is_right_extreme::Bool = true)::Float64
    """
        Three point numeric differenciation using the extremes given a function f,
        a point x and an epsilon.

        Parameters
        ----------
        f : Function
            Function to be evaluated.
        x : Float64
            Point to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """

    if is_right_extreme
        coefficients = [1, -4, 3]
        xs = [x - 2*epsilon, x - epsilon, x]
    else
        coefficients = [-3, 4, -1]
        xs = [x, x + epsilon, x + 2*epsilon]
    end 

    denominator = (2*epsilon)

    return sum([cx[1]*f(cx[2]) for cx  in zip(coefficients, xs)])/denominator
end

function three_point_numeric_diff_extremes(points::Vector{Vector{Float64}}, epsilon::Float64, is_right_extreme::Bool = true)::Float64
    """
        Three point numeric differenciation using the extremes given a set of points [[x, y], ...]
        and an epsilon.

        Parameters
        ----------
        points : Array{Float64, 1}
            Set of points to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """
    if length(points) != 3
        error("The length of the points array must be 3")
    end

    if is_right_extreme
        coefficients = [1, -4, 3]
    else
        coefficients = [-3, 4, -1]
    end
    ys = [points[1][2], points[2][2], points[3][2]]
    denominator = (2*epsilon)

    return sum([cx[1]*cx[2] for cx  in zip(coefficients, ys)])/denominator
end

#---------------------------------------------------------------------------#
#                           Five points derivatives                         #
#                               with middle point                           #
#---------------------------------------------------------------------------#

function five_point_numeric_diff_middle(f::Function, x::Float64, epsilon::Float64)::Float64
    """
        Five point numeric differenciation using the middle point given a function f,
        a point x and an epsilon.

        Parameters
        ----------
        f : Function
            Function to be evaluated.
        x : Float64
            Point to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """
    xs = [(x + i*epsilon) for i in -2:1:2]
    coefficients = [1, -8, 0, 8, -1]
    denominator = 12*epsilon
    
    return sum([cx[1]*f(cx[2]) for cx  in zip(coefficients, xs)])/denominator
end

function five_point_numeric_diff_middle(points::Vector{Vector{Float64}}, epsilon::Float64)::Float64
    """
        Five point numeric differenciation using the middle point given a set of points [[x, y], ...]
        and an epsilon.

        Parameters
        ----------
        points : Array{Float64, 1}
            Set of points to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """
    if length(points) != 5
        error("The length of the points array must be 5")
    end

    coefficients = [1, -8, 0, 8, -1]
    ys = [points[1][2], points[2][2], points[3][2], points[4][2], points[5][2]]
    denominator = 12*epsilon
    
    return sum([cx[1]*cx[2] for cx  in zip(coefficients, ys)])/denominator
end

#---------------------------------------------------------------------------#
#                           Five points derivatives                         #
#                             with extreme points                           #
#---------------------------------------------------------------------------#

function five_point_numeric_diff_extremes(f::Function, x::Float64, epsilon::Float64, is_right_extreme::Bool = true)::Float64
    """
        Five point numeric differenciation using the extremes given a function f,
        a point x and an epsilon.

        Parameters
        ----------
        f : Function
            Function to be evaluated.
        x : Float64
            Point to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """

    if is_right_extreme
        xs = [(x - i*epsilon) for i in 0:1:4]
        coefficients = [3, -16, 36, -48, 25]
    else
        xs = [(x + i*epsilon) for i in 0:1:4]
        coefficients = [-25, 48, -36, 16, -3]
    end


    denominator = 12*epsilon
    
    return sum([cx[1]*f(cx[2]) for cx  in zip(coefficients, xs)])/denominator
end

function five_point_numeric_diff_extremes(points::Vector{Vector{Float64}}, epsilon::Float64, is_right_extreme::Bool = true)::Float64
    """
        Five point numeric differenciation using the extremes given a set of points [[x, y], ...]
        and an epsilon.

        Parameters
        ----------
        points : Array{Float64, 1}
            Set of points to be evaluated.
        epsilon : Float64
            Epsilon to be used in the numeric differenciation.
        
        Returns
        -------
        Float64
            Numeric differenciation of f at x using epsilon.
    """
    if length(points) != 5
        error("The length of the points array must be 5")
    end

    if is_right_extreme
        coefficients = [3, -16, 36, -48, 25]
    else
        coefficients = [-25, 48, -36, 16, -3]
    end 

    ys = [points[1][2], points[2][2], points[3][2], points[4][2], points[5][2]]
    denominator = 12*epsilon
    
    return sum([cx[1]*cx[2] for cx  in zip(coefficients, ys)])/denominator
end

#---------------------------------------------------------------------------#
#                           Richardson extrapolation                         #
#---------------------------------------------------------------------------#


function richardson(f, x, h, n)
    if n == 1
        return derivate(f, x, h)
    end

    term1 = richardson(f, x, h/2, n-1)
    term2 = (term1 - richardson(f, x, h, n-1))/(4^(n-1) - 1)

    return  term1 + term2
end

function general_richardson(f::Function, x::Float64, h::Float64, n::Int, derivate_fn::Function)::Float64
    if n == 1
        return derivate_fn(f, x, h)
    end

    term1 = general_richardson(f, x, h/2, n-1, derivate_fn)
    term2 = (term1 - general_richardson(f, x, h, n-1, derivate_fn))/(4^(n-1) - 1)

    return  term1 + term2
end