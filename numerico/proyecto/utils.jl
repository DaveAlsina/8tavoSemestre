include("factorization.jl")
using Plots

function main( State::Int,
               L::Float64,
               t_max::Float64,
               Nx::Int64,
               Nt::Int64,
               T0_x::Float64,
               T0_t::Float64,
               alpha::Float64;
               heatmap::Bool = false)

    if State == 1
        # println("State 1")
        data = Stationari(L, Nx, T0_x, alpha)
    elseif State == 2
        # println("State 2")
        data = Transitori(L, t_max, Nx, Nt, T0_x, T0_t, alpha)
    end

    
    if heatmap == false
        result = []

        for i in 1:length(data)
            partial_result =  (
                x = [data[i][j][1] for j in 1:length(data[i])],
                y = [data[i][j][2] for j in 1:length(data[i])],
                mode = "lines+markers",
                name = "T($((i-1)*(t_max/Nt)))",
            )

            push!(result, partial_result)
        end

        return result
    
    else

        full_z = []
        for i in 1:length(data)
            z = [data[i][j][2] for j in 1:length(data[i])]
            push!(full_z, z)
        end
    
        result = [(
            z = full_z,
            type = "heatmap", 
            colorscale = "Inferno"
        )]

        return result
    end

end

function Stationari(
    L::Float64,
    Nx::Int64,
    T1::Float64,
    alpha::Float64)

    # ==================== #
    # eq ->  (d^(2)*T)/(d*(x)^2) - alpha^(2)*T = 0
    # ==================== #

    A = zeros(Float64, Nx, Nx)
    b = zeros(Float64, Nx)

    Δx = L/Nx
    γ = alpha^2 * Δx^2

    
    # ==================== #
    # eq -> T_(i+1) - 2*T_(i) + T_(i-1) -γ*T_(i) = 0
    # ==================== #
    
    for i in 2:Nx-1
        
        A[i, i-1]  = 1
        A[i, i] = -2 - γ
        A[i, i+1] = 1
    end

    # ==================== #
    # Conditions
    # ==================== #

    # Initial condition (T1)
    b[1] = -T1
    A[1,1] = -2 - γ
    A[1,2] = 1

    # Frontier condition (dT/dx = 0)
    A[Nx, Nx-1] = 2
    A[Nx, Nx] = -2 - γ

    # ==================== #
    # Solve
    # ==================== #

    M = Inverse(A)
    sol = M*b

    # ==================== #
    # points
    # ==================== #

    points = [ (Δx*i ,sol[i]) for i in 1:Nx ]
    # push at the start
    pushfirst!(points, (0, T1))

    return [points,]
end

function Transitori(
    L::Float64,
    t_max::Float64,
    Nx::Int64,
    Nt::Int64,
    T0_x::Float64,
    T0_t::Float64,
    alpha::Float64)

    # ==================== #
    # eq ->  (d^(2)*T)/(d*(x)^2) - alpha^(2)*T = (d*T)/(d*(t))
    # ==================== #

    Δx = L/Nx
    Δt = t_max/Nt
    γ = alpha^2 * Δx^2
    A = zeros(Float64, Nx, Nx)

    # ==================== #
    # initial conditon t = 0 
    # ==================== #

    b = [ -T0_t * Δx^2 for i in 1:Nx]
    b[1] = b[1] - T0_x*Δt
    
    # ==================== #
    # eq -> Δt(T_(i-1,j) - 2*T_(i,j) + T_(i+1,j) -γ*T_(i,j)) = \Delta x^2 * (T_(i,j) - T_(i,j-1))
    # ==================== #
    solutions = []
    a = [ (Δx*i,T0_t)  for i in 1:Nx]
    pushfirst!(a, (0, T0_x))
    push!(solutions, a)

    for j in 1:Nt

        for i in 2:Nx-1
            A[i, i-1]  = Δt
            A[i, i] = -2*Δt - γ - Δx^2
            A[i, i+1] = Δt
        end

        # ==================== #
        # Conditions
        # ==================== #

        # Initial condition (T1)
        A[1,1] = -2*Δt - γ - Δx^2
        A[1,2] = Δt

        # Frontier condition (dT/dx = 0)
        A[Nx, Nx-1] = 2*Δt
        A[Nx, Nx] = -2*Δt - γ - Δx^2

        # ==================== #
        # Solve
        # ==================== #

        M = Inverse(A)
        sol = M*b

        points = [ ( Δx*i ,sol[i]) for i in 1:Nx ]
        # push at the start
        pushfirst!(points, ( 0, T0_x))

        push!(solutions, points)
   
        b = [ -sol[i] * Δx^2 for i in 1:Nx ]
        b[1] = b[1] - T0_x*Δt
    end

    return solutions
end
