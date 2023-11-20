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
                  parade_condition = nothing)::Tuple{Array{Float64,1},Array{Float64,1}, Array{Float64,1}}


    # Initial values
    t = tstart

    # Arrays to store the results
    ys1 = [y1,]
    ys2 = [y2,]
    ts = [t,]

    # Iteration counter
    i = 1

    while true 

        in1 = (t, y1, y2)
        k1y1 = f1(in1...)*h
        k1y2 = f2(in1...)*h

        in2 = (t + h/2, y1 + (k1y1/2), y2 + (k1y2/2))
        k2y1 = f1(in2...)*h
        k2y2 = f2(in2...)*h

        in3 = (t + h/2, y1 + (k2y1/2), y2 + (k2y2/2))
        k3y1 = f1(in3...)*h
        k3y2 = f2(in3...)*h

        in4 = (t + h, y1 + k3y1, y2 + k3y2)
        k4y1 = f1(in4...)*h
        k4y2 = f2(in4...)*h

        y1 += (k1y1 + 2*k2y1 + 2*k3y1 + k4y1)/6
        y2 += (k1y2 + 2*k2y2 + 2*k3y2 + k4y2)/6
        t += h

        push!(ys1, y1)
        push!(ys2, y2)
        push!(ts, t)

        if !isnothing(parade_condition)
            if parade_condition(t, y1, y2)
                break
            end
        end

        i += 1
    end

    return (ts, ys1, ys2)
end
