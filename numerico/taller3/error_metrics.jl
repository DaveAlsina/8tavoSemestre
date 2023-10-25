using LinearAlgebra

# ----------------------------------------------------------------------- #
#                              Error metrics                              #
# ----------------------------------------------------------------------- #

function error_metric(xaprox::Float64, xtarget::Float64, is_absolute::Bool)
    
    """
        This function calculates the error between the aproximation and the real value
        

        Parameters
        ----------
        xaprox: Float64, The aproximation of the of the function.
        xtarget: Float64, The real value we want.
        is_absolute: Bool, If true then the error is absolute, if false then the error is relative.

        Returns
        -------
        Float64, The error between the aproximation and the real value of the root of the function.
    """
    
    if is_absolute
        return abs(xtarget - xaprox) 
    else
        return abs(xtarget - xaprox)/xtarget
    end
    
end

function error_metric_vectorial(aprox::Vector, target::Vector, is_absolute::Bool)
    
    """
        This function calculates the error between the aproximation and the real value
        

        Parameters
        ----------
        xaprox: Vector, The aproximation of the of the function.
        xtarget: Vector, The real value we want.
        is_absolute: Bool, If true then the error is absolute, if false then the error is relative.

        Returns
        -------
        Float64, The error between the aproximation and the real value of the root of the function.
    """
    
    if is_absolute
        return norm(target - aprox) 
    else
        return norm(target - aprox)/norm(target)
    end
    
end