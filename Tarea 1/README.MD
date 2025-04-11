# TAREA 1 HMI FOR SIGNAL PROCESSING 
### Prerrequisitos 
- Instalar librerias necesarias (customtkinter librosa matplotlib scipy numpy)
### Objetivo de la aplicación 
Desarrollar una interfaz de usuario que permita cargar archivos de audio en formato .wav, aplicar filtros pasa-altas, pasa-bajas y pasa-banda, y visualizar gráficamente tanto la señal original como su transformada de Fourier. Además, la aplicación deberá permitir guardar la señal procesada como un nuevo archivo de audio
![alt text](image.png)
## Menú principal 
El menú principal consta de tres botones el primero permite aplicar el filtro seleccionado, el segundo aplica la tranformada de fourier a mabas señales y el tercero permite guardar el archivo filtrado en formato .wav, una lista deplegable para la selección de filto y dos sliders para modificar la frecuencia de corte, tanto la alta como la baja. 
![alt text](image-4.png)
### Cagrgar archivo 
- Al presionar este botón se abre una ventana para seleccionar un archivo de audio .wav.
- Una vez cargado, se muestra la forma de onda de la señal original.
![alt text](image-1.png)

### Aplicar filtro y frecuencia de corte
Al aplicar el filtro se puede elegir entre los siguientes: 

- Pasa-Bajas

- Pasa-Altas

- Pasa-Banda

![alt text] (image-5.png)

## Alplicar transformada 
Una vez que se aplica el filtro el botón de "Aplicar transformada" le aplica la transformada de fourier tanto a la señal origianl como a la filtrada 
![alt text](image-3.png)

