include("utils.jl")
using Dash 

app = dash(external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"])

DATA  = [
            (x = [1, 2, 3], y = [4, 1, 2], name = "t1"),
            (x = [1, 2, 3], y = [2, 4, 5], name = "t2"),
]

app.layout = html_div() do
    html_center([
        html_h1("Proyecto final de métodos numéricos"),
        html_div("Seleccione los valores de las constantes para la simulación:"),
        html_br(), html_br(), html_br(), html_br(),
    ]),

    # input values
    html_center([
        html_table([
            html_tr([
                html_td(["L (longitud de la barra):  ",
                        dcc_input(id = "L", value = 5, type = "number", min = 0),
                ]),

                html_td(["Tmax (tiempo de simulación):  ",
                        dcc_input(id = "Tmax", value = 2, type = "number", min = 2),
                ]),
                
                html_td(["Nx (número de nodos en x):  ",
                        dcc_input(id = "Nx", value = 10, type = "number", min = 3),
                ]),
            ]),

            html_tr([
                html_td(["Nt (número de nodos en t):  ",
                        dcc_input(id = "Nt",  value = 4, type = "number", min = 0),
                ]),

                html_td(["Tc (temperatura contorno):  ",
                        dcc_input(id = "Tc", value = 100, type = "number", min = 0),
                ]),
                
                html_td(["Ti (temperatura inicial):  ",
                        dcc_input(id = "Ti", value = 0, type = "number", min = 0),
                ]),
            ]),

            html_tr([
                html_td(["Tipo de simulación:  ",
                    dcc_dropdown(id = "STATE",
                                 options = [
                                     (label = "Estado estacionario", value = 1),
                                     (label = "Estado transitiorio", value = 2),
                                 ],
                                 value = 1),
                ]),
                html_td(["alpha (conductividad térmica):  ",
                    dcc_input(id = "alpha", value = 0.1, type = "number", min = 0),
                ]),
            ]),

        ]),
    ]), 

    # Graph
    dcc_graph(id = "ans1",
              figure = (
                  data = DATA, 
                  layout = (title = "Resultado de simulación",)
              )),
    html_center([
        html_h5("El eje horizontal corresponde al eje de la longitud de la barra, y el vertical a la temperatura", style = Dict("width" => "100%", "height" => "100%")),
    ]),
    
    html_br(), html_br(), html_br(), html_br(),
    #color map 
    dcc_graph(id = "ans2",
              figure = (
                        data = [(
                             z = [[0, 1, 2, 3, 4, 5, 6],
                                 [1, 9, 4, 7, 5, 2, 4],
                                 [2, 4, 2, 1, 6, 9, 3]],
                             type = "heatmap", 
                             colorscale = "Inferno"
                        )],
                  layout = (title = "Resultado de simulación",),
                  
                  
              )),

    html_center([
        html_h5("El eje horizontal corresponde al eje de la longitud de la barra, y el vertical a los distintos puntos de tiempo, el color es según la temperatura, como se puede interpretar por la barra en el lateral derecho", style = Dict("width" => "100%", "height" => "100%")),
    ]),

    html_center([
        html_br(), html_br(), html_br(), html_br(),
        html_h4("Por: David Alsina y Nicolás Velandia"),
    ]),

    html_center([
        html_a("Ver código fuente", href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ", target = "_blank"),
    ]),

    #add button to link to another url 
    html_center([
        html_br(), html_br(), html_br(), html_br(),
        html_br(), html_br(), html_br(), html_br(),
        html_br(), html_br(), html_br(), html_br(),
        html_a("No tocar", href = "https://es.pornhub.com", target = "_blank",),
    ])

end

callback!(
          app,
          Output("ans1","figure"),
          Input("L", "value"),
          Input("Tmax", "value"),
          Input("Nx", "value"),
          Input("Nt", "value"),
          Input("Tc", "value"),
          Input("Ti", "value"),
          Input("alpha", "value"),
          Input("STATE", "value"),
          ) do L, Tmax, Nx, Nt, Tc, Ti, alpha, state
    return (
        data = main(Int64(state), Float64(L), Float64(Tmax), Int64(Nx), Int64(Nt), Float64(Tc), Float64(Ti), Float64(alpha)),
        layout = (title = "Resultado de simulación",)
        )
end

callback!(
          app,
          Output("ans2","figure"),
          Input("L", "value"),
          Input("Tmax", "value"),
          Input("Nx", "value"),
          Input("Nt", "value"),
          Input("Tc", "value"),
          Input("Ti", "value"),
          Input("alpha", "value"),
          Input("STATE", "value"),
          ) do L, Tmax, Nx, Nt, Tc, Ti, alpha, state
    return (
        data = main(Int64(state), Float64(L), Float64(Tmax), Int64(Nx), Int64(Nt), Float64(Tc), Float64(Ti), Float64(alpha), heatmap = true),
        layout = (title = "Resultado de simulación mapa de calor",)
        )

end


run_server(app)
