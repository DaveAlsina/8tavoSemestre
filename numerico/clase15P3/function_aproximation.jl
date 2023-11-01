include("error_metrics.jl")
include("integration.jl")


#------------------------------------------------------#
#                 Function metrics                     #
#------------------------------------------------------#

function fn_norm(fn::Function, a::Float64, b::Float64; tol::Float64 = 1e-6)::Float64
    """
    This function calculates the norm of a function.
    """
    return sqrt(adaptative_integral(x -> fn(x)^2, a, b, tol))
end

#------------------------------------------------------#
#                 Polinomial aproximation              #
#------------------------------------------------------#

function aproximate_fn_with_polinomial(fn::Function,
                                       a::Float64,
                                       b::Float64,
                                       n::Integer;
                                       tol::Float64 = 1e-6)::Function
    """
    This function aproximates a function with a polinomial of degree n.
    """
    
    mat = zeros(n, n)


    # Fill the matrix
    for i in 1:n
        for j in 1:n
            mat[i, j] = adaptative_integral(x -> x^(i+j-2), a, b, tol)
        end
    end

    # Fill the vector
    vec = zeros(n)

    for i in 1:n
        vec[i] = adaptative_integral(x -> fn(x)*x^(i-1), a, b, tol)
    end

    # Solve the system
    coef = mat\vec
    
    #build the function
    aprox_fn = x -> sum([coef[i]*x^(i-1) for i in 1:n])
    
    return aprox_fn
end


function aproximate_fn_with_arbitrary_fns(fn::Function,
                                          arbitraty_fns::Array{Function, 1},
                                          a::Float64,
                                          b::Float64,
                                          n::Integer;
                                          tol::Float64 = 1e-6, 
                                          arbitraty_fns_norm::Array{Function, 1} = [])::Function
    coef = zeros(n)

    # Fill the vector
    for i in 1:n

        if length(arbitraty_fns_norm) == 0
            arbitrary_fn_norm = fn_norm(arbitraty_fns[i], a, b, tol = tol)
        else
            arbitrary_fn_norm = arbitraty_fns_norm[i](a, b, tol)
        end

        coef[i] = (1/arbitrary_fn_norm) * adaptative_integral(x -> fn(x)*arbitraty_fns[i](x), a, b, tol)
    end

    #build the function
    aprox_fn = x -> sum([coef[i]*arbitraty_fns[i](x) for i in 1:n])

    return aprox_fn
end


function aproximate_fn_with_legendre(fn::Function,
                                     a::Float64,
                                     b::Float64,
                                     n::Integer;
                                     tol::Float64 = 1e-3)::Function

    legrenge_base = [x -> 0, x -> 1]
    fns_norm = [(a_, b_, tol_) -> 2/(-1*2 + 1), (a_, b_, tol_) -> 2/(0*2 + 1)]
    
    for i in 1:n
        fn_i = x -> (2*(i-1) + 1)*x*legrenge_base[i-1](x) - (i-1)*legrenge_base[i-2](x)
        fn_i_norm = (a_, b_, tol_) -> 2/((i*2) + 1)

        push!(legrenge_base, fn_i)
        push!(fns_norm, fn_i_norm)
    end
    

    return aproximate_fn_with_arbitrary_fns(fn, legrenge_base, a, b, n,
                                            tol = tol, arbitraty_fns_norm = fns_norm)
    
    
end