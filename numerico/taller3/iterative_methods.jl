include("error_metrics.jl")

function decompose_matrix(A::Matrix)

    """
        Decomposes the matrix into D, L and U matrices.
    """
    n = size(A)[1]
    D = zeros(n, n)
    L = zeros(n, n)
    U = zeros(n, n)

    for i in 1:n
        
        #fill the diagonal of D
        D[i, i] = A[i, i]

        #fill the lower matrix
        for j in 1:i-1
            L[i, j] = -A[i, j]
        end

        #fill the upper matrix
        for j in i+1:n
            U[i, j] = -A[i, j]
        end
    end

    return D, L, U
end

function jacobi(A::Matrix,
                b::Vector,
                x::Vector,
                tol::Float64;
                is_absolute:: Bool = true,
                norm::String = "euclidian",
                max_iters::Int64 = Integer(1e6))

    D, L, U = decompose_matrix(A)

    if norm == "euclidian"
        norm_ = 2
    elseif norm == "infinite"
        norm_ = Inf
    else
        print("The norm is not valid")
        return
    end

    #print("D = ", D)

    #calculate the inverse of D
    D_inv = inv(D)

    #calculate the matrix T
    T = D_inv * (L + U)

    #calculate the vector c
    c = D_inv * b

    #store the old value of x
    x_old = x

    #count the number of iterations
    iters = 0

    while true
        x = T * x + c

        if error_metric_vectorial(x, x_old, is_absolute, type = norm_)  < tol
            break
        end

        if iters > max_iters
            print("The method did not converge in the given range of max iterations")
            break
        end

        x_old = x
        iters += 1
    end

    return x   
end

function gauss_siedel(A::Matrix,
                      b::Vector,
                      x::Vector,
                      tol::Float64;
                      is_absolute:: Bool = true,
                      norm::String = "euclidian",
                      max_iters::Int64 = Integer(1e6))

    D, L, U = decompose_matrix(A)

    if norm == "euclidian"
        norm_ = 2
    elseif norm == "infinite"
        norm_ = Inf
    else
        print("The norm is not valid")
        return
    end

    #print("D - L = ", D - L)

    D, L, U = decompose_matrix(A)
    DL_inv = inv(D - L)

    #calculate the T matrix 
    T = DL_inv*U
    c = DL_inv*b

    #store the old value of x
    x_old = x

    #count the number of iterations
    iters = 0

    while true
        x = T * x + c

        if error_metric_vectorial(x, x_old, is_absolute, type = norm_)  < tol
            break
        end

        if iters > max_iters
            print("The method did not converge in the given range of max iterations")
            break
        end
        x_old = x
        iters += 1
    end

    return x
end