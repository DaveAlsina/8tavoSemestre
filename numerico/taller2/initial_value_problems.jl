include("error_metrics.jl")

# ----------------------------------------------------------------------- #
#                              Euler Method                               #
# ----------------------------------------------------------------------- #

function euler_method(df::Function,
                      x0::Float64, 
                      y0::Float64,
                      a::Float64,
                      b::Float64,
                      n::Int64)::Tuple{Array{Float64,1},Array{Float64,1}}
    
    """
    This function solves the initial value problem
    y' = f(x,y), y(x0) = y0
    using the Euler method.

    Input:
    ------------------
        - df: the function derivative y', from which we want to get f(x,y)
        - x0: the initial x value
        - y0: the initial y value
        - a: the left endpoint of the interval
        - b: the right endpoint of the interval
        - n: the number of subintervals

    Output:
    ------------------
        - x: the x values of the solution
        - y: the y values of the solution
    """
    
    epsilon = (b-a)/n
    
    # Initialize the solution vector
    y = zeros(n+1)
    y[1] = y0

    # Initialize the x vector
    x = zeros(n+1)
    x[1] = x0

    for i in 1:n
        y[i+1] = y[i] + epsilon*df(x[i], y[i])
        x[i+1] = i*epsilon + x0
    end

    return x, y
end

function euler_method(df::Function,
                      x0::Float64, 
                      y0::Float64,
                      a::Float64,
                      b::Float64,
                      h::Float64)::Tuple{Array{Float64,1},Array{Float64,1}}
    
    """
    This function solves the initial value problem
    y' = f(x,y), y(x0) = y0
    using the Euler method.

    Input:
    ------------------
        - df: the function derivative y', from which we want to get f(x,y)
        - x0: the initial x value
        - y0: the initial y value
        - a: the left endpoint of the interval
        - b: the right endpoint of the interval
        - n: the number of subintervals

    Output:
    ------------------
        - x: the x values of the solution
        - y: the y values of the solution
    """
    
    epsilon = h
    n = Int64((b-a)/epsilon)
    
    # Initialize the solution vector
    y = zeros(n+1)
    y[1] = y0

    # Initialize the x vector
    x = zeros(n+1)
    x[1] = x0

    for i in 1:n
        y[i+1] = y[i] + epsilon*df(x[i], y[i])
        x[i+1] = i*epsilon + x0
    end

    return x, y
end


# ----------------------------------------------------------------------- #
#                      Taylor Superior Order Method                       #
# ----------------------------------------------------------------------- #

function taylor_superior_order_method(dfs::Array{Function,1},
                                      x0::Float64, 
                                      y0::Float64,
                                      a::Float64,
                                      b::Float64,
                                      n::Int64)::Tuple{Array{Float64,1},Array{Float64,1}}
    """
        This function solves the initial value problem
        y' = f(x,y), y(x0) = y0

        Input:
        --------------------
        - df: The function derivatives y', y'', ..., from which we want to get f(x,y)
        - x0: The initial x value
        - y0: The initial y value
        - a: The left endpoint of the interval
        - b: The right endpoint of the interval
        - n: The number of subintervals
    
        Output:
        --------------------
        - x: The x values of the solution
        - y: The y values of the solution
    """

    epsilon = (b-a)/n
    
    # Initialize the solution vector
    y = zeros(n+1)
    y[1] = y0

    # Initialize the x vector
    x = zeros(n+1)
    x[1] = x0

    for i in 1:n
        change = 0.0

        for j in 1:length(dfs)
            function_to_evaluate = dfs[j]
            change += (epsilon^j)/factorial(j)*function_to_evaluate(x[i], y[i])
        end

        y[i+1] = y[i] + change
        x[i+1] = i*epsilon + x0
    end

    return x, y
end



# ----------------------------------------------------------------------- #
#                      Runge-Kutta-Fehlberg method                        #
# ----------------------------------------------------------------------- #

function runge_kutta_fehlberg_iteration(f::Function, x::Float64, y::Float64, h::Float64, verbose::Bool = false)::vector{float64}
    
    """
        This function solves the initial value problem, using the Runge-Kutta-Fehlberg method.
        
        Input:
        -------

            - f: the function derivative y', from which we want to get f(x,y)
            - x: the initial x value
            - y: the initial y value
            - h: the step size
            - verbose: if true, prints the values of k1, k2, k3, k4, k5, k6, y_new and y_high_ord_new

        Output:
        -------

            - y_new: the new y value
            - y_high_ord_new: the new y value calculated with a higher order method
    """

    k1 = h * f(x, y)
    k2 = h * f(x + h/4, y + 1/4 * k1)
    k3 = h * f(x + 3*h/8, y + 3*k1/32 + 9*k2/32)
    k4 = h * f(x + 12 * h / 13, y + 1932 * k1 / 2197 - 7200 * k2 / 2197 + 7296 * k3 / 2197)
    k5 = h * f(x + h, y + 439 * k1 / 216 - 8 * k2 + 3680 * k3 / 513 - 845 * k4 / 4104)
    k6 = h * f(x + h / 2, y - 8 * k1 / 27 + 2 * k2 - 3544 * k3 / 2565 + 1859 * k4 / 4104 - 11 * k5 / 40)

    if verbose
        println("k1: ", k1)
        println("k2: ", k2)
        println("k3: ", k3)
        println("k4: ", k4)
        println("k5: ", k5)
        println("k6: ", k6)
    end

    y_new = y + 25 * k1 / 216 + 1408 * k3 / 2565 + 2197 * k4 / 4104 - k5 / 5
    y_high_ord_new = y + 16 * k1 / 135 + 6656 * k3 / 12825 + 28561 * k4 / 56430 - 9 * k5 / 50 + 2 * k6 / 55
    
    if verbose
        println("y_new: ", y_new)
        println("y_high_ord_new: ", y_high_ord_new)
    end

    return y_new, y_high_ord_new
end

function runge_kutta_fehlberg(f::Function,
                              x0::Float64,
                              y0::Float64,
                              h_max::Float64,
                              h_min::Float64,
                              n::Int,
                              tol::Float64,
                              is_absolute::Bool)::Tuple{Array{Float64,1},Array{Float64,1}}
    """
        This function solves the initial value problem, using the Runge-Kutta-Fehlberg method.
        
        Input:
        -------

            - f: the function derivative y', from which we want to get f(x,y)
            - x0: the initial x value
            - y0: the initial y value
            - h_max: the maximum step size
            - h_min: the minimum step size
            - n: the number of subintervals
            - tol: the tolerance
            - is_absolute: if true, the error metric is the absolute error, otherwise is the relative error

        Output:
        -------

            - points: the points of the solution
    """

    x = x0
    y = y0 

    points = []
    h = h_max

    x_new = x
    while x_new < n 
                
        y_new, y_high_ord_new = runge_kutta_fehlberg_iteration(f, x, y, h, verbose)
        x_new = x + h
        R = error_metric(y_new, y_high_ord_new, is_absolute)        

        while  R > tol
            q = 0.84* ((tol*h)/(R))^(1/4) 
            h = q*h
            
            if h < h_min
                error("h_min is too high")
            end

            y_new, y_high_ord_new = runge_kutta_fehlberg_iteration(f, x_new, y_new, h)
            x_new = x_new + h
            R = error_metric(y_new, y_high_ord_new, is_absolute)
        end
        y = y_new
        x = x_new

        push!(points, [x, y])
    end

     #return points
     return [points[i][1] for i in 1:length(points)], [points[i][2] for i in 1:length(points)]
end


# ----------------------------------------------------------------------- #
#                      Runge-Kutta 4th order method                       #
# ----------------------------------------------------------------------- #

function rk4_iteration(f::Function, x::Float64, y::Float64, h::Float64)::Float64
    """
        This function solves the initial value problem, using the Runge-Kutta 4th order method.
        
        Input:
        -------

            - f: the function derivative y', from which we want to get f(x,y)
            - x: the initial x value
            - y: the initial y value
            - h: the step size

        Output:
        -------

            - y_new: the new y value
    """

    k1 = h * f(x, y)
    k2 = h * f(x + h / 2, y + k1 / 2)
    k3 = h * f(x + h / 2, y + k2 / 2)
    k4 = h * f(x + h, y + k3)

    y_new = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return y_new
end

function runge_kutta_4(f::Function,
                       x0::Float64,
                       y0::Float64,
                       h::Float64,
                       tol::Float64;
                       error_type::Bool = true,
                       parade_condition = nothing)::Tuple{Array{Float64,1},Array{Float64,1}}
    
    """
        This function solves the initial value problem, using the Runge-Kutta 4th order method.
        
        Input:
        -------

            - f: the function derivative y', from which we want to get f(x,y)
            - x0: the initial x value
            - y0: the initial y value
            - h: the step size
            - tol: the tolerance, if the error is less than the tolerance, the method stops
            - error_type: if true, the error metric is the absolute error, otherwise is the relative error

        Output:
        -------

            - points: the points of the solution
    """

    x = x0
    y = y0
    points = []

    while true
        
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)

        y_new = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x_new = x + h

        push!(points, [x_new,y_new])

        #parade conditions
        if isnothing(parade_condition)
            if error_metric(y_new, y, error_type) < tol
                break
            end
        else
            if parade_condition(x, x_new, y, y_new)
                break
            end
        end

        y = y_new
        x = x_new

    end

    #return points
    return [points[i][1] for i in 1:length(points)], [points[i][2] for i in 1:length(points)]
end

# ----------------------------------------------------------------------- #
#                     Runge-Kutta 3th order method                        #
# ----------------------------------------------------------------------- #

function runge_kutta_3(f::Function,
                       x0::Float64,
                       y0::Float64,
                       h::Float64,
                       tol::Float64;
                       error_type::Bool = true, 
                       parade_condition = nothing)::Tuple{Array{Float64,1},Array{Float64,1}}
    """
        This function solves the initial value problem, using the Runge-Kutta 3th order method.
        
        Input:
        -------

            - f: the function derivative y', from which we want to get f(x,y)
            - x0: the initial x value
            - y0: the initial y value
            - h: the step size
            - tol: the tolerance, if the error is less than the tolerance, the method stops
            - error_type: if true, the error metric is the absolute error, otherwise is the relative error

        Output:
        -------

            - points: the points of the solution
    """

    
    x = x0
    y = y0

    points = []

    while true

        x_new = x + h
        y_new = y + h/2* (f(x,y) + f(x_new,y+h*f(x,y)))

        #parade conditions
        if isnothing(parade_condition)
            if error_metric(y_new, y, error_type) < tol
                break
            end
        else
            if parade_condition(x, x_new, y, y_new)
                break
            end
        end

        y = y_new
        x = x_new

        push!(points, [x,y])
        
        
    end

    #return points
    return [points[i][1] for i in 1:length(points)], [points[i][2] for i in 1:length(points)]
end

# ----------------------------------------------------------------------- #
#                     Runge-Kutta 2th order method                        #
# ----------------------------------------------------------------------- #

function runge_kutta_2(f::Function,
                       x0::Float64,
                       y0::Float64,
                       h::Float64,
                       tol::Float64;
                       error_type::Bool = true,
                       parade_condition = nothing)::Tuple{Array{Float64,1},Array{Float64,1}}
    """
        This function solves the initial value problem, using the Runge-Kutta 2th order method.
        
        Input:
        -------

            - f: the function derivative y', from which we want to get f(x,y)
            - x0: the initial x value
            - y0: the initial y value
            - h: the step size
            - tol: the tolerance, if the error is less than the tolerance, the method stops
            - error_type: if true, the error metric is the absolute error, otherwise is the relative error
            

        Output:
        -------

            - points: the points of the solution
    """
    
    x = x0
    y = y0

    points = []

    while true

        y_new = y + h * f(x + h / 2, y + h / 2 * f(x, y))    
        x_new = x + h

        #parade conditions
        if isnothing(parade_condition)
            if error_metric(y_new, y, error_type) < tol
                break
            end
        else
            if parade_condition(x, x_new, y, y_new)
                break
            end
        end
    
        y = y_new
        x = x_new

        push!(points, [x,y])
    end

    #return points
    return [points[i][1] for i in 1:length(points)], [points[i][2] for i in 1:length(points)]
end