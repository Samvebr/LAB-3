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
Para nuestra practica tuvimos que tomar los audios dos veces puesto que el SNR daba un valor menor que cero, el la realacion señal ruido que mejor pudimos obtener fue la siguiente:
 - SNR de Samuel.wav: 16.48 dB
 - SNR de Santiago.wav: 7.57 dB
 - SNR de Salome.wav: 9.24 dB

Estos valores sugieren que el microfono del celular de samuel tiene mer calidad de grabacion a comparación de los microfonos del celular de santiago o salome. Tambien se puede deber a otros factores como el ruido de fondo, la intensidad de la voz grabada y la distancia al micrófono.

## Analisis Temporal y Espectral de las Señales
Las librerias que se emplean para esta parte del laboratorio son:
  - Numpy: se usa para cálculos matemáticos y manejo de arrays
  - Matplotlib.pyplot: se usa para graficar señales en el dominio del tiempo y frecuencia.
  - Scipy.io.wavfile: se usa para leer archivos de audio en formato WAV.
```bash
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
```
Se definen en *archivos* los cuatro archivos de audio, tres son los microfonos mientras se habla y uno es el ruido de fondo de la habitacion donde se grabo.
```bash
archivos = ["Samuel.wav", "Santiago.wav", "Salome.wav", "Ruido_Ambiente.wav"]
```
El codigo procesa el archivo *"Ruido_Ambiente.wav"* para calcular su potencia, para mas adelante con este calcular el SNR de las señales de voz.

```bash
potencia_ruido = None
try:
    # Lee el archivo de audio de ruido
    sample_rate_ruido, audio_ruido = wavfile.read("Ruido_Ambiente.wav")
    
    # Convertir a mono si el audio es estéreo (se toma solo el primer canal)
    if len(audio_ruido.shape) > 1:
        audio_ruido = audio_ruido[:, 0]
    
    # Convertir el audio a tipo float para realizar cálculos precisos
    audio_ruido = audio_ruido.astype(np.float32)

    # Calcular la potencia del ruido utilizando la media de los cuadrados de la señal
    potencia_ruido = np.mean(audio_ruido ** 2)

except FileNotFoundError:
    print("Error: No se encontró el archivo Ruido_Ambiente.wav.")
except ValueError:
    print("Error: Archivo Ruido_Ambiente.wav no es un WAV válido.")
except Exception as e:
    print(f"Error al procesar Ruido_Ambiente.wav: {e}")
```
Se lee el archivo de ruido ambiente, sei el audio es estereo, se convierte a mono para tomar un solo canal, luego se convierte a float para lograr cálculos de presición y se calcula la potencia del ruido como la medida de los cuadrados de la señal.

Para graficar la señal en el dominio del tiempo y de la frecuencia, primero se crea una grafica de 14x10 pulgadas para mostrar varias figuras, despues se crea un ciclo *for* para iterar sobre todos los archivos execpto el del ruido, se normaliza la señal para que sus valores esten entre el rango de (-1,1) y se genera el eje del tiempo.
```bash
for i, archivo in enumerate(archivos[:-1], 1):  # Excluye el archivo de ruido de la visualización
    try:
        # Lee el archivo de audio
        sample_rate, audio_data = wavfile.read(archivo)
        
        # Convertir a mono si el audio es estéreo (se toma el primer canal)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
 # Normalizar la señal
        audio_data_norm = audio_data / np.max(np.abs(audio_data))

        # Crear eje de tiempo
        tiempo = np.arange(len(audio_data_norm)) / sample_rate
```
**Grafica en el Dominio del Tiempo**
Puesto que ya se creo el eje del tiempo anteriormente, esta se grafica en función del tiempo, se coloca en color azul y se activa la cuadricula, ademas se configura el tiulo y las etiquetas.
```bash
        # ========================================
        # Gráfica en el dominio del tiempo
        # ========================================
        plt.subplot(3, 2, 2*i-1)  # Subplot impar para tiempo
        plt.plot(tiempo, audio_data_norm, color='#1f77b4', alpha=0.7)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title(f"Señal Temporal - {archivo}")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xlim(0, tiempo[-1])  # Mostrar todo el rango temporal
```

**Grafica en el Dominio de la Frecuencia**
Se calcula la transformada Rapida de Fourier (FFT) y se generan las frecuencias correspondientes, luego se obtiene la magnitud del espectro y se tomo la mitad positiva, se grafica el esprectro de frecuencias en escala logaritmica y se muestran las graficas.

```bash
        # ========================================
        # Gráfica en el dominio de la frecuencia
        # ========================================
        # Calcular la FFT
        N = len(audio_data_norm)
        fft_data = np.fft.fft(audio_data_norm)
        freqs = np.fft.fftfreq(N, d=1/sample_rate)

        # Tomar mitad positiva del espectro
        fft_magnitude = np.abs(fft_data[:N//2])
        freqs = freqs[:N//2]

        plt.subplot(3, 2, 2*i)  # Subplot par para frecuencia
        plt.plot(freqs, fft_magnitude, label=f"SNR: {snr_db:.2f} dB", 
                color='#ff7f0e', alpha=0.7)
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud")
        plt.title(f"Espectro de Frecuencias - {archivo}")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xscale("log")
        plt.xlim(20, 10000)
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")

# Ajustar el diseño y mostrar
plt.tight_layout()
plt.show()
```
Para el calculo del SNR se toma la potencia de la señal sobre la potencia del ruido y se incerta en la formula como se encuentra dentro del ciclo *for* lo calcula para cada una de las señales de audio y se imprime en pantalla.
```bash
 # Calcular la potencia de la señal utilizando la media de los cuadrados
        potencia_senal = np.mean(audio_data ** 2)

        # Calcular la relación señal-ruido (SNR)
        if potencia_ruido is not None and potencia_ruido > 0:
            if potencia_senal > potencia_ruido:
                snr_db = 10 * np.log10((potencia_senal) / potencia_ruido)
            else:
                snr_db = float('-inf')
        else:
            snr_db = float('-inf')
```
se obtienecomo resultado la siguiente imagen:
![image](https://github.com/user-attachments/assets/0f4f9e1a-9574-40fa-9c6a-79c6a8841d3b)

En la parte izquierda de cada fila se muestra la forma de onda de la señal a lo largo del tiempo. Se observa que la señal "Samuel.wav" tiene un incremento progresivo de amplitud, lo que sugiere una mayor intensidad conforme avanza el tiempo, lo que coincide con su mayor relación SNR (16.48 dB). En "Santiago.wav", la señal presenta una mayor va-riabilidad y fluctuaciones intensas en varios puntos, indicando una voz con mayor dinámica. Por otro lado, "Salo-me.wav" tiene una estructura más estable con picos bien distribuidos, lo que sugiere una menor variabilidad en la intensidad de la voz, esto para las ultimas dos señales sugiere mayor interferencia de ruido o un volumen mas variables asociado con sus SNR mas bajos (7.57 dB y 9.24 dB) . Todas las señales están normalizadas en amplitud entre -1 y 1, lo que facilita la comparación visual.

Las graficas de la derecha muestran el espectro de frecuencias de cada señal en escala logarítmica, mostrando distribucion de energia en diferentes bandas de frecuencia. En "Samuel.wav", se observa un pico dominante por denajo de los 100Hz y energia sitribuida hasta los 1000Hz, lo que es caracteristico de la voz. En "Santiago.wav" muestra un espectro mas complejo con multiples picos, lo que indica la presencia de más armonicos y una sñal mas rica en frecuencias. Y en "Salome.wav" se exhibe varios picos pronunciados con energia distribuida de manera mas homogénea, sugiriendo una voz con una estructura espectral bien definida. 

## Separación de Voz
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
![image](https://github.com/user-attachments/assets/32dadc5d-c78b-4f0c-b991-e4f3bf471381)


Como se observa en la imagen se separan las tres señales encontradas en el archivo de audio y en rojo se resalta la voz predominante mientras que en gris se ponen las voces menos predominantes.

Para calcular el SNR se definio *senal_original* como la suma de todas las señales de entrada, luego se estimo el ruido como la diferencia entre la señal original y la señal limpia separada y se calcula el SNR y se muestra en pantalla.
```bash
# Calcular la señal de ruido como la diferencia entre la señal original combinada y la señal limpia
senal_original = np.sum(audio_signals, axis=0)  # Señal original combinada
ruido = senal_original - voz_filtrada  # Ruido estimado

# Cálculo del SNR
potencia_senal = np.sum(voz_filtrada**2)
potencia_ruido = np.sum(ruido**2)
SNR = 10 * np.log10(potencia_senal / potencia_ruido)
print(f" SNR de la señal predominante: {SNR:.2f} dB")
```
Da un SNR de 10.57 dB lo que quiere decir que el audio obtenido es de calidad baja, puede ser comprensible pero con ruido molesto.

## Bibliografía
“9. Ruido y dB | PySDR: A Guide to SDR and DSP using Python”. PySDR: A Guide to SDR and DSP using Python. Accedido el 1 de marzo de 2025. [En línea]. Disponible: https://pysdr.org/es/content-es/noise.html

“Python: How to separate out noise from human speech in audio file?” Stack Overflow. Accedido el 1 de marzo de 2025. [En línea]. Disponible: https://stackoverflow.com/questions/58054927/python-how-to-separate-out-noise-from-human-speech-in-audio-file

“MANIPULANDO AUDIOS EN PYTHON, CON «pydub».” El Programador Chapuzas. Accedido el 1 de marzo de 2025. [En línea]. Disponible: https://programacionpython80889555.wordpress.com/2020/02/25/manipulando-audios-en-python-con-pydub/
