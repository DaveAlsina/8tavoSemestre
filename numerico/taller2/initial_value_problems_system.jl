include("initial_value_problems.jl")
# ----------------------------------------------------------------------- #
#                          Systems of Equations                           #
# ----------------------------------------------------------------------- #

function RKsystem(f::Function,
                  x0::Float64,
                  y0::Float64,
                  h::Float64,
                  tol::Float64;
                  error_type::Bool = true,
                  parade_condition = nothing)::Tuple{Array{Float64,1},Array{Float64,1}}

    y1_new = rk4_iteration(f,x0,y0,h)


        


end
