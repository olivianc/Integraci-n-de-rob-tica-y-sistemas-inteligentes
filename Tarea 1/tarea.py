#importación de bibliotecas necesarias
import customtkinter as ctk
import numpy as np
import librosa
import scipy.signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

# Configuración inicial de la interfaz
ctk.set_appearance_mode("dark")  # Modo claro u oscuro
ctk.set_default_color_theme("green")  # Tema de color

class AudioProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HMI - Procesamiento de Señales")
        self.geometry("1200x800")  # Ventana ampliada
        #Variables de almacenamiento de audio 
        self.audio_data = None
        self.sample_rate = None
        self.filtered_signal = None  # Variable para almacenar la señal filtrada
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame superior para el botón y la señal original
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Botón para cargar archivo
        self.load_button = ctk.CTkButton(top_frame, text="Cargar Archivo", command=self.load_audio)
        self.load_button.pack(side="top", pady=10, anchor="center")

        # Canvas para la señal original
        self.figure_original, self.ax_original = plt.subplots(figsize=(7, 5))
        self.canvas_original = FigureCanvasTkAgg(self.figure_original, top_frame)
        self.canvas_original.get_tk_widget().pack(pady=10, anchor="center")
        self.ax_original.set_title("Señal Original")

        # Controles de procesamiento
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(pady=15, anchor="center")

        ctk.CTkLabel(controls_frame, text="Seleccione el tipo de filtro:").pack()
        self.filter_type = ctk.StringVar(value="Pasa-Bajas")
        self.filter_menu = ctk.CTkComboBox(controls_frame, variable=self.filter_type, values=["Pasa-Bajas", "Pasa-Altas", "Pasa-Banda"])
        self.filter_menu.pack(pady=5)

        self.low_freq_label = ctk.CTkLabel(controls_frame, text="Frecuencia Baja: 100 Hz")
        self.low_freq_label.pack()
        self.low_cutoff_freq = ctk.DoubleVar(value=100)
        self.low_slider = ctk.CTkSlider(controls_frame, variable=self.low_cutoff_freq, from_=10, to=5000, command=self.update_low_frequency_label)
        self.low_slider.pack(pady=5)

        self.high_freq_label = ctk.CTkLabel(controls_frame, text="Frecuencia Alta: 1000 Hz")
        self.high_freq_label.pack()
        self.high_cutoff_freq = ctk.DoubleVar(value=1000)
        self.high_slider = ctk.CTkSlider(controls_frame, variable=self.high_cutoff_freq, from_=10, to=5000, command=self.update_high_frequency_label)
        self.high_slider.pack(pady=5)

        # Botones de acciones
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)

        self.apply_filter_button = ctk.CTkButton(buttons_frame, text="Aplicar Filtro", command=self.apply_filter)
        self.apply_filter_button.grid(row=0, column=0, padx=10)

        self.apply_transform_button = ctk.CTkButton(buttons_frame, text="Aplicar Transformada", command=self.apply_fourier_transform)
        self.apply_transform_button.grid(row=0, column=1, padx=10)

        self.save_button = ctk.CTkButton(buttons_frame, text="Guardar Audio Filtrado", command=self.save_filtered_audio, state="disabled")
        self.save_button.grid(row=0, column=2, padx=10)

        # Frame para gráficas
        graphs_frame = ctk.CTkFrame(self)
        graphs_frame.pack(fill="both", padx=10, pady=15)

        self.figure_filtered, self.ax_filtered = plt.subplots(figsize=(5, 3))
        self.canvas_filtered = FigureCanvasTkAgg(self.figure_filtered, graphs_frame)
        self.ax_filtered.set_title("Señal Filtrada")

        self.figure_fourier, self.ax_fourier = plt.subplots(figsize=(5, 3))
        self.canvas_fourier = FigureCanvasTkAgg(self.figure_fourier, graphs_frame)
        self.ax_fourier.set_title("Transformada de Fourier (Señal Filtrada)")

        self.figure_fourier_original, self.ax_fourier_original = plt.subplots(figsize=(5, 3))
        self.canvas_fourier_original = FigureCanvasTkAgg(self.figure_fourier_original, graphs_frame)
        self.ax_fourier_original.set_title("Transformada de Fourier (Señal Original)")

        # Configurar distribución de columnas para que las gráficas se acomoden correctamente
        graphs_frame.columnconfigure(0, weight=1)
        graphs_frame.columnconfigure(1, weight=1)
        graphs_frame.columnconfigure(2, weight=1)

        self.canvas_filtered.get_tk_widget().grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        self.canvas_fourier.get_tk_widget().grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        self.canvas_fourier_original.get_tk_widget().grid(row=0, column=2, padx=15, pady=10, sticky="nsew")

    def update_low_frequency_label(self, value):
        self.low_freq_label.configure(text=f"Frecuencia Baja: {int(value)} Hz")

    def update_high_frequency_label(self, value):
        self.high_freq_label.configure(text=f"Frecuencia Alta: {int(value)} Hz")

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Audio", "*.wav")])
        if file_path:
            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)  # Cargar el audio sin cambiar el sample rate
            self.plot_original_signal()

    def apply_filter(self):
        if self.audio_data is not None:
            filter_type = self.filter_type.get()
            # Crear el filtro adecuado según el tipo seleccionado
            if filter_type == "Pasa-Bajas":
                cutoff = self.low_cutoff_freq.get()
                b, a = scipy.signal.butter(4, cutoff, btype='low', fs=self.sample_rate)
            elif filter_type == "Pasa-Altas":
                cutoff = self.high_cutoff_freq.get()
                b, a = scipy.signal.butter(4, cutoff, btype='high', fs=self.sample_rate)
            elif filter_type == "Pasa-Banda":
                low_cutoff = self.low_cutoff_freq.get()
                high_cutoff = self.high_cutoff_freq.get()
                b, a = scipy.signal.butter(4, [low_cutoff, high_cutoff], btype='band', fs=self.sample_rate)
             # Aplicar el filtro con filtfilt para evitar desfase
            self.filtered_signal = scipy.signal.filtfilt(b, a, self.audio_data)
            self.plot_filtered_signal(self.filtered_signal, title=f"Señal Filtrada ({filter_type})")
            self.save_button.configure(state="normal")

    def apply_fourier_transform(self):
        if self.audio_data is not None:
            # FFT de la señal original
            fft_spectrum_original = np.fft.fft(self.audio_data)
            fft_magnitude_original = np.abs(fft_spectrum_original)
            freqs_original = np.fft.fftfreq(len(fft_magnitude_original), 1 / self.sample_rate)
            
             # Graficar FFT original
            self.ax_fourier_original.clear()
            self.ax_fourier_original.plot(freqs_original[:len(freqs_original)//2], fft_magnitude_original[:len(freqs_original)//2])
            self.ax_fourier_original.set_title("Transformada de Fourier (Señal Original)")
            self.ax_fourier_original.set_xlabel("Frecuencia (Hz)")
            self.ax_fourier_original.set_ylabel("Magnitud")
            valor_maximo = np.max(fft_magnitude_original) * 1.1  # Aumentar un 10% para tener margen
            self.ax_fourier_original.set_ylim(0, valor_maximo)
            self.canvas_fourier_original.draw()
            

            # FFT de la señal filtrada
            if self.filtered_signal is not None:
                fft_spectrum_filtered = np.fft.fft(self.filtered_signal)
                fft_magnitude_filtered = np.abs(fft_spectrum_filtered)
                freqs_filtered = np.fft.fftfreq(len(fft_magnitude_filtered), 1 / self.sample_rate)

                self.ax_fourier.clear()
                self.ax_fourier.plot(freqs_filtered[:len(freqs_filtered)//2], fft_magnitude_filtered[:len(freqs_filtered)//2])
                self.ax_fourier.set_title("Transformada de Fourier (Señal Filtrada)")
                self.ax_fourier.set_xlabel("Frecuencia (Hz)")
                self.ax_fourier.set_ylabel("Magnitud")
                self.canvas_fourier.draw()

    def save_filtered_audio(self):
        if self.filtered_signal is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Archivo WAV", "*.wav")])
            if file_path:
                scaled_signal = np.int16(self.filtered_signal / np.max(np.abs(self.filtered_signal)) * 32767)
                write(file_path, self.sample_rate, scaled_signal)

    def plot_original_signal(self):
        self.ax_original.clear()
        self.ax_original.plot(self.audio_data)
        self.ax_original.set_title("Señal Original")
        self.ax_original.set_xlabel("Muestras")
        self.ax_original.set_ylabel("Amplitud")
        self.canvas_original.draw()

    def plot_filtered_signal(self, signal, title=""):
        self.ax_filtered.clear()
        self.ax_filtered.plot(signal)
        self.ax_filtered.set_title(title)
        self.ax_filtered.set_xlabel("Muestras")
        self.ax_filtered.set_ylabel("Amplitud")
        self.canvas_filtered.draw()

if __name__ == "__main__":
    app = AudioProcessorApp()
    app.mainloop()