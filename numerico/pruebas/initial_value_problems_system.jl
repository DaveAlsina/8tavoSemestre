include("initial_value_problems.jl")
# ----------------------------------------------------------------------- #
#                          Systems of Equations                           #
# ----------------------------------------------------------------------- #

function RKsystem(f1::Function,
                  f2::Function,
                  y1::Float64,
                  y2::Float64,
                  tstart::Float64,
                  tend::Float64,
                  h::Float64;
                  error_type::Bool = true,
                  parade_condition = nothing)

    # Arrays to store the results
    args = [tstart, y1, y2]

    # Arrays to store the results
    answer = [args,]

    # Iteration counter
    i = 1

    while true 

        args = rk4_iteration_generalized(args...; fns = [f1, f2], h = h)
        push!(answer, collect(args))

        if !isnothing(parade_condition)
            if parade_condition(args...)
                break
            end
        end

        i += 1
    end

    return answer
end


function rk4_iteration_generalized(args...; fns, h)


    # Initial values
    t = args[1]

    # Arrays to store the results
    ys = args[2:end]
    ts = [t,]


    k1 = []
    for fn in fns
        #build the input
        input = (t, ys...)
        
        #compute k1
        push!(k1, fn(input...)*h)
    end

    k2 = []
    for fn in fns
        #build the input
        input = [t + h/2,]

        for i in 1:length(ys)
            push!(input, ys[i] + (k1[i]/2))
        end

        #compute k2
        push!(k2, fn(input...)*h)
    end

    k3 = []
    for fn in fns
        #build the input
        input = [t + h/2,]
        for i in 1:length(ys)
            push!(input, ys[i] + (k2[i]/2))
        end

        #compute k3
        push!(k3, fn(input...)*h)
    end

    k4 = []
    for fn in fns
        #build the input
        input = [t + h,]
        for i in 1:length(ys)
            push!(input, ys[i] + k3[i])
        end

        #compute k4
        push!(k4, fn(input...)*h)
    end

    output = [t + h,]
    for i in 1:length(ys)
        push!(output, ys[i] + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6)
    end

    return output
end
