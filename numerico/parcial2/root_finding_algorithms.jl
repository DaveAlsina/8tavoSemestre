include("error_metrics.jl")

function update_c(f, a::Float64, b::Float64)
    return (a+b)/2
end

function bisection(f, a, b, tol, max_iter, target_value)
    
    """
    This function finds the root of a function f using the way of updating the midpoint c, 
    given by update_c and the interval [a,b]. The tolerance is given by tol. 
    The maximum number of iterations is given by max_iter.

    Parameters:
    ------------
        f: function which we want to find the root for
        update_c: function which updates the value of c (the midpoint, which should be very close to the root)
        a: left endpoint of the interval
        b: right endpoint of the interval
        tol: tolerance for the root
        max_iter: maximum number of iterations

        
    Returns:
    ------------
        c: midpoint of the interval, which should be very close to the root of f
        iters: number of iterations needed to find the root
    """

    c = update_c(f, a, b)
    value = f(c)
    iters = 1

    while (abs(target_value-value) > tol) && (iters < max_iter)

        if (value*f(a) < 0)
            b = c 
        elseif (value*f(b) < 0)
            a = c
        end

        c = update_c(f, a, b)
        value = f(c)
        iters += 1
    end

    return c, iters
end
