import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from sklearn.decomposition import FastICA

# Función para aplicar un filtro pasa-banda (300 Hz - 3400 Hz, rango vocal humano)
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# Lista de archivos WAV
archivos = ["Samuel.wav", "Santiago.wav", "Salome.wav"]

# Lista para almacenar las señales de audio
audio_signals = []
sample_rates = []

# Leer los archivos de audio
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

# Asegurar que todas las señales tengan la misma longitud
min_length = min(map(len, audio_signals))
audio_signals = [signal[:min_length] for signal in audio_signals]

# Convertir la lista en una matriz para ICA
X = np.vstack(audio_signals).T  # Filas = muestras, columnas = señales

# Aplicar ICA
ica = FastICA(n_components=len(archivos))
S_ica = ica.fit_transform(X)  # Señales separadas

# Aplicar filtro pasa-banda a cada fuente separada
S_ica_filtered = np.array([butter_bandpass_filter(S_ica[:, i], 300, 3400, sample_rates[0]) for i in range(len(archivos))]).T

# Calcular la energía de cada señal separada (después del filtrado)
energia = [np.sum(np.square(S_ica_filtered[:, i])) for i in range(len(archivos))]

# Seleccionar la señal con mayor energía (voz predominante)
idx_voz = np.argmax(energia)
voz_filtrada = S_ica_filtered[:, idx_voz]

# Eliminar cualquier sonido residual (ajustando un umbral de energía mínima)
umbral = 0.05 * np.max(np.abs(voz_filtrada))  # Solo dejar valores por encima del 5% del máximo
voz_filtrada[np.abs(voz_filtrada) < umbral] = 0  # Silenciar ruido residual

# Normalizar la señal antes de guardar
voz_filtrada /= np.max(np.abs(voz_filtrada))

# Convertir a int16 para guardar como WAV
voz_wav = (voz_filtrada * 32767).astype(np.int16)

# Guardar archivo WAV con la voz más dominante y sin ruido de fondo
wavfile.write("voz_dominante_sin_ruido.wav", sample_rates[0], voz_wav)
print("Archivo guardado: voz_dominante_sin_ruido.wav")

# Calcular la señal de ruido como la diferencia entre la señal original combinada y la señal limpia
senal_original = np.sum(audio_signals, axis=0)  # Señal original combinada
ruido = senal_original - voz_filtrada  # Ruido estimado

# Cálculo del SNR
potencia_senal = np.sum(voz_filtrada**2)
potencia_ruido = np.sum(ruido**2)
SNR = 10 * np.log10(potencia_senal / potencia_ruido)

# Mostrar el valor del SNR en pantalla
print(f" SNR de la señal predominante: {SNR:.2f} dB")

# Graficar todas las señales separadas y resaltar la predominante
plt.figure(figsize=(10, 6))

for i in range(len(archivos)):
    plt.subplot(len(archivos), 1, i+1)
    plt.plot(S_ica_filtered[:, i], label=f"Fuente Separada {i+1}", color="gray" if i != idx_voz else "r", linewidth=2)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.legend()
    plt.grid()
    if i == idx_voz:
        plt.title("Voz más predominante (Filtrada y sin ruido)")

plt.tight_layout()
plt.show()


