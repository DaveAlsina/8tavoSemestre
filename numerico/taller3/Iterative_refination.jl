include("norms.jl")
include("factorization.jl")

function iterative_refination(A::Matrix, b::Vector, tol::Float64; norm::String, max_iters::Int64 = Integer(1e6))
    """
        Calculates the solution of the linear system Ax = b using the iterative refination method.
    """

    if norm == "norm_2"
        normF = norm_2
    elseif norm == "norm_infinite"
        normF = norm_infinite
    else
        print("The norm is not valid")
        return
    end
    
    M = Inverse(A)
    x = M*b # primera aproximación    
    r = b - A*x  # residuo
    y = M*r # nuevo b
    count = 0

    while true
        x = x+ y
        r = b - A*x
        y = M*r
        if  (normF(y, x)/normF(y) > tol) || (count > max_iters)
            break
        end
        count += 1
    end

    return x
end

function iterative_refination2(A::Matrix, b::Vector, tol::Float64; norm::String, max_iters::Int64 = Integer(1e6))
    """
        Calculates the solution of the linear system Ax = b using the iterative refination method.
    """

    if norm == "norm_2"
        normF = norm_2
    elseif norm == "norm_infinite"
        normF = norm_infinite
    else
        print("The norm is not valid")
        return
    end
    
    M = Inverse(A)
    x = M*b # primera aproximación    
    r = b - A*x  # residuo
    y = M*r # nuevo b
    count = 0
    x = x+ y

    while normF(y) > tol
        r = b - A*x
        y = M*r
        x = x+ y
        if (count > max_iters)
            break
        end
        count += 1
    end

    return x
end