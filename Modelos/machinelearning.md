
Naive Bayes classifier.

Los ingredientes esenciales de los cuales incluyen combinar el teorema de Bayes con
una suposición de independencia sobre las características (esta es la parte "ingenua").
Aunque es simple, sigue siendo un método popular para la categorización de texto.
Por ejemplo, usando frecuencias de palabras como características, este enfoque puede clasificar con precisión
correos electrónicos como correo no deseado, o si un texto en particular fue escrito por un autor específico.
De hecho, con un preprocesamiento cuidadoso, el algoritmo a menudo es competitivo con métodos más avanzados,
incluyendo máquinas de vectores de soporte.

[notebook](nbayes/ML-NaiveBayes.ipynb)

Neural networks

Una red neuronal está formada por capas de pequeños elementos informáticos que procesan datos de una manera que recuerda a las neuronas del cerebro. Una forma de aprendizaje automático, mejora en función de los comentarios, si sus juicios eran correctos. En este caso, los investigadores entrenaron su algoritmo utilizando datos del Departamento de Policía de Los Ángeles (LAPD) en California desde 2014 hasta 2016 en más de 50,000 homicidios relacionados con pandillas y no relacionados con pandillas, asaltos agravados y robos.

[notebook](neural_networks/MachineLearning-NeuralNetworks.ipynb)

Random forests

Los bosques aleatorios combinan las predicciones de árboles de decisión múltiple. Recuerde de nuestro capítulo anterior que al construir un árbol de decisión, el conjunto de datos se divide repetidamente en subárboles, guiados por la mejor combinación de variables. Sin embargo, encontrar la combinación correcta de variables puede ser difícil. Por ejemplo, un árbol de decisión construido en base a una muestra pequeña podría no ser generalizable a futuras muestras grandes. Para superar esto, se podrían construir árboles de decisión múltiples, aleatorizando la combinación y el orden de las variables utilizadas. El resultado agregado de estos bosques de árboles formaría un conjunto, conocido como bosque aleatorio.

[notebook](forests/MachineLearning-RandomForest.ipynb)
