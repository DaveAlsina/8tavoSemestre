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
    system_matrix[j,:] = system_matrix[j,:] - (factor.*system_matrix[i,:])
    vec[j] = vec[j] - (factor.*vec[i])

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

    for i = 1:n
        # Elimination 
        for j = i+1:n
            system_matrix, vector = gaussian_elimination_step(system_matrix, vector, i, j)
        end
    end

    return system_matrix, vector
end


function partial_pivoting(system_matrix::Matrix, vector::Vector)
    n = length(vector)

    for i = 1:n-1
        # Find the maximum value in the i-th column
        max_value, max_row = findmax(abs.(system_matrix[i:n,i]))

        if max_row == 1
            max_row = i
        else
            max_row = max_row + i - 1
        end

        # Swap the rows
        if max_row != i
            system_matrix[[i, max_row],:] = system_matrix[[max_row, i],:]
            vector[[i, max_row]] = vector[[max_row,i]]
        end

        # Elimination
        for j = i+1:n
            system_matrix, vector = gaussian_elimination_step(system_matrix, vector, i, j)
        end

    end

    return system_matrix, vector
end

function scaled_partial_pivoting(system_matrix::Matrix, vector::Vector)
    n = length(vector)

    # Find the scaling factors
    scaling_factors = maximum(abs.(system_matrix), dims=2)
    println("scaling_factors = ", scaling_factors)

    for i = 1:n-1
        # Find the maximum value in the k-th column
        max_value, max_row = findmax(abs.(system_matrix[i:n,i])./scaling_factors[i:n])

        if max_row == 1
            max_row = i
        else
            max_row = max_row + i - 1
        end

        # Swap the rows
        if max_row != i
            system_matrix[[i, max_row],:] = system_matrix[[max_row, i],:]
            vector[[i, max_row]] = vector[[max_row,i]]
            scaling_factors[[i, max_row]] = scaling_factors[[max_row,i]]
        end

        # Elimination
        for j = i+1:n
            system_matrix, vector = gaussian_elimination_step(system_matrix, vector, i, j)
        end

    end

    return system_matrix, vector
end

function direct_matrix_solution(system_matrix::Matrix, vector::Vector{Float64}; type::String)

    system_matrix = deepcopy(system_matrix)
    vector = deepcopy(vector)

    if type == "gaussian_elimination"
        system_matrix, vector = gaussian_elimination(system_matrix, vector)

    elseif type == "partial_pivoting"
        system_matrix, vector = partial_pivoting(system_matrix, vector)

    elseif type == "scaled_partial_pivoting"
        system_matrix, vector = scaled_partial_pivoting(system_matrix, vector)
    else
        error("Invalid method, available methods are: gaussian, partial pivoting, scaled partial pivoting")
    end

    # Back substitution
    n = length(vector)
    x = zeros(n,1)

    for i = n:-1:1
        num = vector[i]
        for j = i+1:n
            num = num - system_matrix[i,j]*x[j]
        end
        x[i] = num/system_matrix[i,i]
    end

    return system_matrix, vector, x

end