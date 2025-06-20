## 🚀 PROYECTO DATA SCIENTIST/AI DEVELOPER: Aprendizaje Supervisado

Proyecto educativo hecho por:

- [Omar Lengua](https://www.linkedin.com/in/omarlengua/)
- [Max Beltran](https://www.linkedin.com/in/max-beltran/)
- [Cesar Mercado](https://www.linkedin.com/in/cesarmercadohernandez/)
- [Alla Haruty](https://www.linkedin.com/in/allaharuty/)

Este proyecto implementa un modelo de Machine Learning supervisado de clasificación que permite predecir la probabilidad de un accidente cerebrovascular (stroke) a partir de un formulario con datos personales o a partir de una imágenes de resonancia magnética del paciente. 

### ¿Qué dataset utilizamos?

- [Dataset inicial](https://www.kaggle.com/datasets/jillanisofttech/brain-stroke-dataset/data)
- [Dataset secundario para implementar data augmentation y tratamiento de datos desbalanceados](https://data.mendeley.com/datasets/x8ygrw87jw/1)
- [Dataset de imágenes](https://www.kaggle.com/datasets/afridirahman/brain-stroke-ct-image-dataset/data)

Al analizar el dataset inicial notamos un problema importante: los datos estaban fuertemente desbalanceados. Específicamente, había 4.733 casos sin ictus frente a solo 248 con ictus, lo que representa un serio obstáculo para entrenar un modelo fiable.

### ¿Por qué decidimos combinar dos datasets?

Debido al desbalanceo del dataset original, sabíamos que el modelo podría tener dificultades para identificar correctamente los casos positivos (ictus), lo que en un contexto de salud podría tener consecuencias graves. En situaciones como esta, es preferible que el modelo dé falsos positivos antes que falle al detectar un caso real de ictus.

Por eso, decidimos incorporar datos adicionales de un [segundo dataset](https://data.mendeley.com/datasets/x8ygrw87jw/1), asegurándonos de que tuviera al menos las mismas columnas para facilitar la integración. Sin embargo, al combinar ambos conjuntos, el desbalanceo seguía siendo un problema. Para solucionarlo, optamos por añadir únicamente las instancias donde stroke = 1 del segundo dataset, incrementando así el número total de casos positivos.

### Resultado de la combinación

Con esta estrategia pasamos de tener 248 casos positivos a 783 casos de ictus, mejorando significativamente el equilibrio entre clases. Esto nos proporciona una base más sólida para entrenar un modelo con mejor capacidad predictiva, especialmente en la detección de casos positivos.

Para ello, hicimos un análisis exploratorio de datos completo que se puede ver paso a paso en la rama [feature/EDA](https://github.com/alharuty/Proyecto-IX-DS2/tree/feature/EDA) donde cada integrante del equipo estudió y analizó el dataset, y finalmente pudimos verificar y considerar un análisis de datos final que lo llamamos EDA.ipyb .

Para el encontrar el mejor modelo y las mejores métricas, seguimos el mismo paso en la rama [feature/model](https://github.com/alharuty/Proyecto-IX-DS2/tree/feature/model) donde cada integrante estudió y propuso el mejor modelo encontrado. Finalmente elejimos el **modelo RandomForest + RandomUnderSampler** llamado model.pkl hecho por Cesar, con un accuracy de 77%.

<img src="./capturas/metricas-random-forest.png" alt="Métricas random forest" width="400">

Además, como un paso extra y de nivel avanzado, Max pudo entrenar un **modelo de red neuronal (CNN) con PyTorch** llamado cnn_pytorch.pth, para realizar las predicciones mediante las imágenes, con un accuracy del 93% y un overfitting menor que 2%.

<img src="./capturas/metricas-cnn.png" alt="Métricas del modelo pytorch con cnn" width="400">

<img src="./capturas/overfitting.png" alt="Overfitting imagenes" width="400">

Se puede encontrar el entrenamiento final de los 2 modelos en la carpeta model/.

La aplicación está realizado con backend FastApi y frontend REact y Vite y además está dockerizado y subido las 2 imágenes de los 2 servicios en Dockerhub.

<img src="./capturas/Diagrama_stroke_predict.drawio.png" alt="Diagrama de arquitectura" width="400">

‼️TODO: Añadir demo

‼️TODO: Añadir instrucciones para descargar repo

‼️TODO: Añadir instrucciones para descargar docker

‼️TODO: tree de las carpetas

‼️TODO: Link a la presentación de gamma

‼️TODO: Link a deepwiki

Hemos conseguido terminar este proyecto con la metodología scrum y un reparto de roles:
- Alla como Scrum Master y desarrolladora Backend con FastApi
- Omar como desarrollador Frontend con React
- Max como Ingeniero de Datos e Ingeniero de Machine Learning CNN
- Cesar como Ingeniero de Machine Learning RandomForest

Aunque los roles estaban bien definidos, uno de los aspectos más valiosos del proyecto ha sido la colaboración transversal. El análisis de datos ha sido un esfuerzo compartido por todo el equipo, permitiéndonos tener una comprensión profunda del conjunto de datos, identificar variables relevantes, realizar limpieza y preprocesamiento, y definir las estrategias de modelado más adecuadas.