import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Lista de audios a procesar
archivos = ["Samuel.wav", "Santiago.wav", "Salome.wav", "Ruido_Ambiente.wav"]

# Inicializa la variable para almacenar la potencia del ruido
potencia_ruido = None

# Procesa primero el archivo de ruido para obtener su potencia
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

# Crear una figura para los subgráficos con 2 columnas (tiempo y frecuencia)
plt.figure(figsize=(14, 10))

# Itera sobre cada archivo de audio (exceptuando el de ruido)
for i, archivo in enumerate(archivos[:-1], 1):  # Excluye el archivo de ruido de la visualización
    try:
        # Lee el archivo de audio
        sample_rate, audio_data = wavfile.read(archivo)
        
        # Convertir a mono si el audio es estéreo (se toma el primer canal)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        
        # Convertir la señal a tipo float para realizar cálculos
        audio_data = audio_data.astype(np.float32)

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

        # Normalizar la señal
        audio_data_norm = audio_data / np.max(np.abs(audio_data))

        # Crear eje de tiempo
        tiempo = np.arange(len(audio_data_norm)) / sample_rate

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
