
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

function jacobi(A::Matrix, b::Vector)

    """
        Calculates the solution of the linear system Ax = b using the Jacobi method.
    """

    D, L, U = decompose_matrix(A)

    #calculate the inverse of D
    D_inv = inv(D)

    #calculate the matrix T
    T = D_inv * (L + U)

    #calculate the vector c
    c = D_inv * b
end