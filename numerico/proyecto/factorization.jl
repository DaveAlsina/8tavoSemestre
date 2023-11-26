function LU(A::Matrix)
    L = zeros(size(A))
    U = zeros(size(A))
    n = size(A)[1]
    for i in 1:n
        for j in 1:n
            if i == j
                L[i, j] = 1
                U[i,j] = A[i,j]
            elseif i < j
                U[i, j] = A[i, j]
            else
                L[i, j] = A[i,j] / A[j, j]
            end
        end
    end
    return L, U
end

function solution(A::Matrix, b::Vector)
    n = length(b)
    x = zeros(n)

    for i = 1:n
        x[i] = b[i]
        for j = 1:i-1
            x[i] -= A[i, j] * x[j]
        end
        x[i] /= A[i, i]
    end

    return x
end

function Inverse(A::Matrix)
    L, U = LU(A)
    n = size(A)[1]
    M = zeros(size(A))
    for i = 1:n
        c = zeros(n)
        c[i] = 1
        d = solution(L, c)
        x = solution(U, d)
        M[:,i] = x
    end  
    return M
end