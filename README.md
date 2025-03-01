# LAB 3 - Experimento del Coctel
En el experimento "Fiesta de Cóctel" se grabaron tres audios de forma simultánea desde distintas posiciones, con el objetivo de estudiar la propagación y variaciones del sonido en un ambiente real. A continuación se explica la teoría paso a paso:

## Selección del entorno
En nuestro caso se eligió un espacio ailado de ruido, es decir, una sala insonora para lograr un mejor resultado en la obtencion de las frecuencias y obtener un mejor resultado en la relacion SNR.

## Ubicación de micrófonos
Se posicionaron tres micrófonos en diferentes puntos estratégicos para captar la señal desde diversas perspectivas. Esta distribución permite analizar cómo varía la intensidad, frecuencia y calidad del sonido según la distancia y la dirección respecto a la fuente principal.

![Sin título](https://github.com/user-attachments/assets/4a1a8b4d-fccf-4671-91f4-999c3d43366c)


*Debemos tener en cuenta que en nuestro caso se presentan 3 fuentes de ruido, los cuales son 3 voces disntintas, cada una ubicada a una posicion diferente de cada uno de los microfonos como se muestra a continuacion:*

                      
![Imagen de WhatsApp 2025-02-27 a las 22 18 11_d844402c-500x500](https://github.com/user-attachments/assets/294b7dad-4f51-456e-bca9-19652293eebb)  ![AAAAAAAA-500x500](https://github.com/user-attachments/assets/d2578ed6-09b7-473c-9e88-5a67b1bd56e2)

![bbbbbbbbbbbb-1000x400](https://github.com/user-attachments/assets/ef6d0308-efc7-4ff4-83b1-ac867c858406)



## Grabación simultánea
Las tres grabaciones se realizaron al mismo tiempo para obtener datos coherentes y comparables. Esto facilita el estudio de fenómenos acústicos como la interferencia, la reverberación y el efecto de obstáculos en el entorno.

## Análisis teórico
Basándose en principios de la acústica, se aplica el concepto de relación señal-ruido (SNR) para evaluar la pureza de la señal en cada posición, considerando la influencia del ruido ambiental. La teoría respalda cómo factores como la distancia y la dirección impactan en la calidad del audio captado.
## Separacion de Voz
La separacion de la voz se designo por el metodo de Análisis de Componentes Independientes (ICA),para este metodo se utilizaron las librerias:
- Numpy: Manejo de arreglos numericos
- Matplotlib: Graficar señales 
- Scipy.io. wavfile:Leer y escribir archivos de audio .waw
- Sklearn.descmposition. FastICA: separa señales de audio usando ICA.

Luego se declara la funcion *butter_bandpass_filter* para dejar pasar frecuencia entre *lowcut* y *highcut* y se calcula la frecuencia de muetsreo con la variable Nyquis, que lleva el nombre del mismo teorema. Por ultimo, se normalizan las frecuencias de corte dividiendolas entre la de *Nyquist*, *butter* disena el filtro y *lfilter* se utilza para aplicarlo a todos los datos, de esta forma deja pasar solo las frecuencias en un rango de 300Hz - 3400Hz.

```bash
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)
````
Posteriormente se realiza la lectura de los archivos, donde se crea una lista con los archivos de audio y dos listas vacias para almacenar las señales y sus tasas de muestreo 

```bash
archivos = ["Samuel.wav", "Santiago.wav", "Salome.wav"]
audio_signals = []
sample_rates = []
````
Despues de leer los archivos se crea un bucle para leerlos, que sigue el siguiente orden:
1.Lee cada archivo *.wav* con *wavfile.read()*.
2.Convierte a mono y si es estereo (toma solo un canal).
3. Convierte los datos a valores de tipo float y normaliza la amplitud en el rango de -1 y 1.
4.Almacena la señal y la tasa de muestreo en listas.

```bash
for archivo in archivos:
    try:
        sample_rate, audio_data = wavfile.read(archivo)
        
        # Si el audio es estéreo, convertirlo a mono tomando un solo canal
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        
        # Convertir a float y normalizar
        audio_data = audio_data.astype(np.float32)
        audio_data /= np.max(np.abs(audio_data))

        # Guardar señal y tasa de muestreo
        audio_signals.append(audio_data)
        sample_rates.append(sample_rate)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")
```

Para aplicar ICA se requiere que todas las señales tengan la misma cantidad de muestras, debido a esto con *min-length* se encuentra la señal mas corta y se recorta todas las señales a la misma longitud.

``bash
min_length = min(map(len, audio_signals))
audio_signals = [signal[:min_length] for signal in audio_signals]
```

Luego procedemos con separar una sola señal de audio, para esto se convierten las señales a matriz para que poder aplicar ICA, la matriz se define como:
-Filas: muestras de tiempo.
-Columnas: diferentes señales de audio.
```bash
X = np.vstack(audio_signals).T  # Filas = muestras, columnas = señales
```

Luego se aplica ICA con *FastICA* con *fit_transform(X)* se extrae componentes independientes de la mezcla de señales.

```bash
ica = FastICA(n_components=len(archivos))
S_ica = ica.fit_transform(X)  # Señales separadas
```
Se aplica a un filtro pasabanda a las señales separadas y se usa *np.array* para reoorganizar las señales en la misma estructura.

```bash
S_ica_filtered = np.array([butter_bandpass_filter(S_ica[:, i], 300, 3400, sample_rates[0]) for i in range(len(archivos))]).T
```
Como la voz predominante es la que tiene mayor energia, esta se calcula como la suma de los valores al cuadrado de cada señal. Y posteriormente con *idx_voz* se encuentra el indice de la señal con mayor energia y se extrae la voz predominante.

```bash
energia = [np.sum(np.square(S_ica_filtered[:, i])) for i in range(len(archivos))]
idx_voz = np.argmax(energia)
voz_filtrada = S_ica_filtered[:, idx_voz]
```
Se define un umbral de 5% del valor maximo para silenciar valores menores al umbral, reduciendo de esta manera el ruido de fondo.

```bash
umbral = 0.05 * np.max(np.abs(voz_filtrada))  # Solo dejar valores por encima del 5% del máximo
voz_filtrada[np.abs(voz_filtrada) < umbral] = 0  # Silenciar ruido residual
```
Normalizamos la señal y se convierte a formato estandar para Wav con el comando *int16*, para despúes guardar la señal filtrada en *voz_dominante_sin_ruido.wav*.

```bash
voz_filtrada /= np.max(np.abs(voz_filtrada))
wavfile.write("voz_dominante_sin_ruido.wav", sample_rates[0], voz_wav)
print("✅ Archivo guardado: voz_dominante_sin_ruido.wav")
```
Finalmente se grafican las señales por separado, resaltando en rojo la señal de la voz predominante.
```bash
plt.figure(figsize=(10, 6))

for i in range(len(archivos)):
    plt.subplot(len(archivos), 1, i+1)
    plt.plot(S_ica_filtered[:, i], label=f"Fuente Separada {i+1}", color="gray" if i != idx_voz else "r", linewidth=2)
    plt.legend()
    plt.grid()
    if i == idx_voz:
        plt.title("Voz más predominante (Filtrada y sin ruido)")

plt.tight_layout()
plt.show()
```
![image](https://github.com/user-attachments/assets/433e862e-8ced-447f-8f28-12c01608fcad)

Como se observa en la imagen se separan las tres señales encontradas en el archivo de audio y en rojo se resalta la voz predominante mientras que en gris se ponen las voces menos predominantes.
