include("initial_value_problems.jl")
# ----------------------------------------------------------------------- #
#                          Systems of Equations                           #
# ----------------------------------------------------------------------- #

function RKsystem(fns::Array{Function,1},
                  x0::Float64,
                  y0::Float64,
                  h::Float64,
                  tol::Float64;
                  error_type::Bool = true,
                  parade_condition = nothing)::Tuple{Array{Float64,1},Array{Float64,1}}

    len = length(fns)

    # Initialize the solution arrays
    # it contains [[t0, y0, y1, ..., yn], ...]
    solution_array = []

    while true
        # Initialize the solution array for the current step
        # it contains [t0, y0, y1, ..., yn]
        solution = [x0, y0]

        # Initialize the k arrays
        k = zeros(len, 4)

        # Calculate the k arrays
        for i in 1:4
            k[:,i] = h .* fns(solution[1], solution[2:end]...)
            solution[2:end] += k[:,i] ./ 6
            solution[1] += h
        end

        # Calculate the error
        if error_type
            error = abs(k[:,1] - k[:,2] - k[:,3] + k[:,4]) ./ 6
        else
            error = abs(k[:,1] - k[:,2]) ./ 6
        end

        # Check the error
        if maximum(error) <= tol
            # Append the solution to the solution array
            push!(solution_array, solution)

            # Update the initial values
            x0 = solution[1]
            y0 = solution[2:end]

            # Check the parade condition
            if parade_condition != nothing
                if parade_condition(x0, y0...)
                    break
                end
            end
        end

        # Update the step size
        h = h * (tol / maximum(error))^(1/4)
    end
        


end
