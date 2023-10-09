function gaussian_elimination_step(row1:: Vector{Float64}, row2::Vector{Float64}, output_vector::Vector{Float64}, pivot::Int)
    """
        Performs a step of the full pivoting Gaussian elimination method
        on the system of equations represented by the rows row1 and row2.
        Returns the new rows after the elimination step.

        Input:
        -------------
        row1: Vector{Float64}
            The first row of the system of equations
        row2: Vector{Float64}
            The second row of the system of equations
        pivot: Int
            The index of the second row that is being eliminated
        
        Output:
        -------------
        result: new row after the elimination step.
        new_vector: new vector after the elimination step.
    """
    factor = (row2[pivot][pivot-1]/row2[pivot-1][pivot-1])
    return (row2 - ((factor).*row1)), (output_vector - ((factor).*output_vector))
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
        #elimination 
        for j = i+1:n
            updated_matrix, updated_vector = gaussian_elimination_step(system_matrix[i,i:n], system_matrix[j,i:n], vector[j], i)
            system_matrix[j,i:n] = updated_matrix
            vector[j] = updated_vector
        end
    end
end


function partial_pivoting(system_matrix::Matrix, vector::Vector)
    n = length(vector)

    for k = 1:n-1
        # Find the maximum value in the k-th column
        max_value = abs(system_matrix[k,k])
        max_value, max_row = findmax(abs.(system_matrix[k:n,k]))

        # Swap the rows
        if max_row != k
            system_matrix[[k, max_row],:] = system_matrix[[max_row, k],:]
            vector[[k, max_row]] = vector[[max_row,k]]
        end

        # Elimination
        for i = k+1:n
            factor = system_matrix[i,k]/system_matrix[k,k]
            system_matrix[i,k] = 0
            for j = k+1:n
                system_matrix[i,j] = system_matrix[i,j] - factor*system_matrix[k,j]
            end
            vector[i] = vector[i] - factor*vector[k]
        end

    end
    return system_matrix, vector
end