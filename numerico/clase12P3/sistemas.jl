"""
n = size(a);
    n = n(1);
    x = zeros(n,1);
    if strcmp(metodo, 'gaussiana')
        for i = 1:n
            for j = i+1:n
                m = a(j,i)/(a(i,i));
                a(j,:) = a(j,:) - m*a(i,:);
                b(j,:) = b(j,:) - m*b(i,:);
            end
        end
    elseif strcmp(metodo, 'parcial')
        for i = 1:n
            [M, ind] = max(abs(a(i:end,i)));
            ind = ind+i-1;
            a([i,ind],:) = a([ind,i],:);
            b([i,ind],:) = b([ind,i],:);
            for j = i+1:n
                m = a(j,i)/(a(i,i));
                a(j,:) = a(j,:) - m*a(i,:);
                b(j,:) = b(j,:) - m*b(i,:);
            end
        end
    elseif strcmp(metodo, 'escalado')
        S = max(abs(a), [], 2);
        for i = 1:n
            [M, ind] = max(abs(a(i:end,i))./abs(S(i:end)));
            ind = ind+i-1;
            a([i,ind],:) = a([ind,i],:);
            b([i,ind],:) = b([ind,i],:);
            S([i,ind],:) = S([ind,i],:);
            for j = i+1:n
                m = a(j,i)/(a(i,i));
                a(j,:) = a(j,:) - m*a(i,:);
                b(j,:) = b(j,:) - m*b(i,:);
            end
        end
    end
    for i = n:-1:1
        num = b(i);
        for j = i+1:n
            num = num - a(i,j)*x(j);
        end
        x(i) = num/a(i,i);
    end
end

"""



function gaussian_elimination_step(system_matrix:: Matrix, vec::Vector{Float64}, i::Integer, j::Integer)
    """
        Performs a step of the full pivoting Gaussian elimination method
        on the system of equations represented by the rows row1 and row2.
        Returns the new rows after the elimination step.

        Input:
        -------------
            system_matrix: Matrix
                The matrix representing the system of equations
            vector: Vector{Float64}
                The vector representing the system of equations
            i: Integer
                The row index of the pivot element
            j: Integer
                The row index of the element to be eliminated

        Output:
        -------------
            system_matrix: new matrix after the elimination step.
            vector: new vector after the elimination step.
    """
    #m = a(j,i)/(a(i,i));
    factor = (system_matrix[j,i]/system_matrix[i,i])
    
    #elimination step
    system_matrix[j,:] = system_matrix[j,:] - factor*system_matrix[i,:]
    vec[j] = vec[j] - factor*vec[i]

    return system_matrix, vec
end

function gaussian_elimination(system_matrix::Matrix, vector::Vector{Float64})
    
    """
        Performs the full pivoting Gaussian elimination method
        on the system of equations represented by the matrix system_matrix
        and the vector vector.
        Returns the new matrix and vector after the elimination step.

        Input:
        -------------
        system_matrix: Matrix
            The matrix representing the system of equations
        vector: Vector{Float64}
            The vector representing the system of equations
        
        Output:
        -------------
        system_matrix: new matrix after the elimination step.
        vector: new vector after the elimination step.
    """
    
    n = length(vector)

    for i = 1:n-1
        # Elimination 
        for j = i+1:n
            system_matrix, vector = gaussian_elimination_step(system_matrix, vector, i, j)
        end
    end
end


function partial_pivoting(system_matrix::Matrix, vector::Vector)
    n = length(vector)

    for i = 1:n-1
        # Find the maximum value in the k-th column
        max_value = abs(system_matrix[i,i])
        max_value, max_row = findmax(abs.(system_matrix[i:n,i]))

        # Swap the rows
        if max_row != i
            system_matrix[[i, max_row],:] = system_matrix[[max_row, i],:]
            vector[[i, max_row]] = vector[[max_row,i]]
        end

        # Elimination
        for j = i+1:n
            system_matrix, vector = gaussian_elimination_step(system_matrix, vector, k, j)
        end

    end

    return system_matrix, vector
end

function scaled_partial_pivoting(system_matrix::Matrix, vector::Vector)
    n = length(vector)

    # Find the scaling factors
    scaling_factors = maximum(abs.(system_matrix), dims=2)

    for i = 1:n-1
        # Find the maximum value in the k-th column
        max_value = abs(system_matrix[i,i])/scaling_factors[i]
        max_value, max_row = findmax(abs.(system_matrix[i:n,i])/scaling_factors[i:n])

        # Swap the rows
        if max_row != i
            system_matrix[[i, max_row],:] = system_matrix[[max_row, i],:]
            vector[[i, max_row]] = vector[[max_row,i]]
        end

        # Elimination
        for j = i+1:n
            system_matrix, vector = gaussian_elimination_step(system_matrix, vector, k, j)
        end

    end

    return system_matrix, vector
end

function direct_matrix_solution(system_matrix::Matrix, vector::Vector{Float64}; type::String)

    if type == "gaussian"
        system_matrix, vector = gaussian_elimination(system_matrix, vector)

    elseif type == "partial pivoting"
        system_matrix, vector = partial_pivoting(system_matrix, vector)

    elseif type == "scaled partial pivoting"
        system_matrix, vector = scaled_partial_pivoting(system_matrix, vector)
    else
        error("Invalid method, available methods are: gaussian, partial pivoting, scaled partial pivoting")
    end

end