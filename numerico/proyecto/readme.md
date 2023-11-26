# Proyecto análisis numérico

## Integrantes
Nicolas Velandia, David Alsina

## Cómo ejecutar el código
``` 
julia main.jl
```

## Descripción del proyecto

Este proyecto tiene como objetivo realizar análisis numérico para la simulación de un fenómeno físico relacionado con la transferencia de calor en una barra. El código base proporciona una interfaz gráfica interactiva utilizando Dash, donde el usuario puede seleccionar diferentes parámetros para la simulación y visualizar los resultados.

### Estructura del Código

El código se organiza de la siguiente manera:

- **main.jl**: Contiene la interfaz gráfica Dash y las funciones de callback para la simulación.

- **utils.jl**: Incluye las funciones principales para realizar el análisis numérico, específicamente la resolución de ecuaciones diferenciales para casos estacionarios y transitorios.

### Interfaz Gráfica

La interfaz gráfica consta de varios elementos:

- **Entrada de Datos**: Se proporciona un conjunto de parámetros que el usuario puede ajustar para la simulación, como la longitud de la barra, el tiempo de simulación, el número de nodos en x y t, la temperatura en los bordes, la temperatura inicial, el tipo de simulación y la conductividad térmica.

- **Gráfico de Resultados**: Muestra el resultado de la simulación en forma de gráfico de líneas, donde el eje horizontal representa la longitud de la barra y el eje vertical representa la temperatura en diferentes momentos o estados, dependiendo del tipo de simulación.

- **Mapa de Calor**: Presenta un mapa de calor que ilustra la variación de la temperatura en función de la longitud de la barra y el tiempo en el caso de simulación transitoria.

### Ejecución y Resultados

Al ejecutar el código, la interfaz gráfica se despliega en un servidor local, y los resultados de la simulación se actualizan dinámicamente en respuesta a los cambios en los parámetros introducidos por el usuario.

Para acceder al código fuente completo, puedes visitar el repositorio en [GitHub](https://github.com/DaveAlsina/8tavoSemestre/tree/main/numerico/proyecto).

---

Este proyecto fue desarrollado como parte del curso de Análisis Numérico en colaboración entre David Alsina y Nicolás Velandia.