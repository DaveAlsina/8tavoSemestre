function norm_infinite(X::Vector)
    x = X[1]
    for i in 2:size(X)[1]
        if abs(X[i]) > abs(x)
            x = X[i]
        end
    end
    return x
end

function norm_2(X::Vector)
    x = 0
    for i in 1:size(X)[1]
        x += X[i]^2
    end
    return sqrt(x)
end

function norm_infinite(X::Vector, Y::Vector)
    x = X[1] - Y[1]
    for i in 2:size(X)[1]
        if abs(X[i] - Y[i]) > abs(x)
            x = X[i] - Y[i]
        end
    end
    return x
end

function norm_2(X::Vector, Y::Vector)
    x = 0
    for i in 1:size(X)[1]
        x += (X[i] - Y[i])^2
    end
    return sqrt(x)
end