import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.io import wavfile
from scipy.interpolate import make_interp_spline


import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from amplifier import Amplifier
from distortion import Distortion
from bruit import Bruit

# ---------------------- INTERFACE GRAPHIQUE ----------------------

class AudioProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Processor")
        self.root.geometry("800x500")

        self.audio_file = None
        self.sample_rate = None
        self.audio_data = None
        self.processed_audio = None

        # Sidebar (cadre des boutons)
        self.sidebar = tk.Frame(root, width=200, bg="gray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.load_button = tk.Button(self.sidebar, text="Charger Audio", command=self.load_audio)
        self.load_button.pack(pady=10, padx=10, fill=tk.X)

        self.amplify_button = tk.Button(self.sidebar, text="Amplifier", command=self.apply_amplification, state=tk.DISABLED)
        self.amplify_button.pack(pady=5, padx=10, fill=tk.X)

        self.reduce_button = tk.Button(self.sidebar, text="Réduire bruit", command=self.apply_reduction, state=tk.DISABLED)
        self.reduce_button.pack(pady=5, padx=10, fill=tk.X)

        self.distortion_button = tk.Button(self.sidebar, text="Corriger Distorsion", command=self.apply_distortion, state=tk.DISABLED)
        self.distortion_button.pack(pady=5, padx=10, fill=tk.X)

        self.save_button = tk.Button(self.sidebar, text="Sauvegarder", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack(pady=10, padx=10, fill=tk.X)

        # Zone de graphes
        self.fig, self.ax = plt.subplots(2, 1, figsize=(5, 4))
        self.ax[0].set_title("Audio Original")
        self.ax[1].set_title("Audio Traité")

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def load_audio(self):
        """Charge un fichier audio"""
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.sample_rate, self.audio_data = self.read_wav(file_path)
            if len(self.audio_data.shape) > 1:
                self.audio_data = np.mean(self.audio_data, axis=1).astype(np.int16)
            self.audio_file = file_path
            self.processed_audio = self.audio_data.copy()
            self.amplify_button.config(state=tk.NORMAL)
            self.reduce_button.config(state=tk.NORMAL)
            self.distortion_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.DISABLED)
            self.plot_audio()
            messagebox.showinfo("Succès", "Fichier audio chargé avec succès !")

    def apply_amplification(self):
        """Applique une amplification au son"""
        if self.audio_data is not None:
            # Applique l'amplification
            self.processed_audio = Amplifier.amplify(self.audio_data, self.sample_rate, 1.1)
            
            # Accélère l'audio
            self.processed_audio = Amplifier.speed_up_with_sampling_rate(self.processed_audio, self.sample_rate, 2)
            
            # Affiche le signal traité
            self.plot_audio()
            
            # Active le bouton de sauvegarde
            self.save_button.config(state=tk.NORMAL)
            
            # Affiche un message de succès
            messagebox.showinfo("Succès", "Amplification et accélération appliquées.")

    def apply_reduction(self):
        """Applique une réduction du volume"""
        if self.audio_data is not None:
            self.processed_audio = Bruit.reduce_noise(self.audio_data,self.sample_rate)
            self.plot_audio()
            self.save_button.config(state=tk.NORMAL)
            messagebox.showinfo("Succès", "Réduction du volume appliquée.")

    def apply_distortion(self):
        """Corrige la distorsion du son"""
        if self.audio_data is not None:
            self.processed_audio = Distortion.reduce_distortion(self.audio_data)
            self.plot_audio()
            self.save_button.config(state=tk.NORMAL)
            messagebox.showinfo("Succès", "Correction de distorsion appliquée.")

    def plot_audio(self):
        """Affiche les signaux audio avant et après traitement"""
        self.ax[0].cla()
        self.ax[0].plot(self.audio_data, color="blue")
        self.ax[0].set_title("Audio Original")

        self.ax[1].cla()
        self.ax[1].plot(self.processed_audio, color="red")
        self.ax[1].set_title("Audio Traité")

        self.canvas.draw()


    def save_audio(self):
        """Sauvegarde le fichier audio traité"""
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if save_path:
            self.write_wav(save_path, self.processed_audio,self.sample_rate)
            messagebox.showinfo("Succès", f"Fichier sauvegardé sous : {os.path.basename(save_path)}")

    def normalize_signal(self,signal):
        max_amplitude = np.max(np.abs(signal))
        if max_amplitude == 0:
            return signal
        scale = 32767 / max_amplitude  # Normaliser à 16 bits
        return (signal * scale).astype(np.int16)

    
    def speed_up(self, samples, factor):
        """Accélère l'audio en réduisant le nombre d'échantillons."""
        # Calcul du nombre d'échantillons dans la nouvelle version de l'audio
        new_length = int(len(samples) / factor)
        
        # Création d'un tableau d'indices réduits pour l'accélération
        indices = np.linspace(0, len(samples) - 1, new_length).astype(int)
        
        # Retourne les échantillons correspondants aux indices réduits
        new_samples = samples[indices]

        # Normalisation des échantillons après modification de la vitesse
        new_samples = self.normalize_signal(new_samples)
        
        return new_samples



    def read_wav(self, filename):
        with open(filename, "rb") as f:
            header = f.read(44)
            sample_rate = int.from_bytes(header[24:28], byteorder="little")
            
            # Assure-toi que tu as bien un format PCM (16-bit signé, mono)
            num_channels = int.from_bytes(header[22:24], byteorder="little")
            bits_per_sample = int.from_bytes(header[34:36], byteorder="little")
            
            # Lire les données audio
            if bits_per_sample == 16:
                data = np.frombuffer(f.read(), dtype=np.int16)
            else:
                raise ValueError(f"Format non supporté: {bits_per_sample} bits par échantillon")
        return sample_rate, data



    def normalize_signale(self, signal):
        """Normalize the signal to the range of np.int16."""
        max_val = np.max(np.abs(signal))
        if max_val == 0:  # Éviter la division par zéro
            return np.zeros_like(signal, dtype=np.int16)
        signal = signal / max_val  # Normalize to [-1, 1]
        signal = signal * 32767  # Scale to int16 range
        return signal.astype(np.int16)


    def int_to_bytes(self,value, size=4):
        """Convertit un entier en bytes (little-endian)"""
        return value.to_bytes(size, byteorder='little')

    def write_wav(self, filename, signal, sample_rate):
        """Sauvegarde le fichier audio au format WAV."""
        
        # Normalisation du signal pour éviter les erreurs de lecture
        signal = np.clip(signal * 32767, -32768, 32767).astype(np.int16)

        # Vérification du sample_rate
        if sample_rate <= 0:
            raise ValueError("Le taux d'échantillonnage doit être un entier positif.")

        data_size = signal.size  # Taille des données (chaque échantillon est de 2 octets)
        
        try:
            with open(filename, 'wb') as f:
                # Entête RIFF
                f.write(b'RIFF')
                f.write(self.int_to_bytes(36 + data_size))  # Taille totale du fichier - 8
                f.write(b'WAVE')
                
                # Chunk fmt (16 octets)
                f.write(b'fmt ')
                f.write(self.int_to_bytes(16))  # Taille du chunk fmt
                f.write(self.int_to_bytes(1, 2))  # Format PCM = 1
                f.write(self.int_to_bytes(1, 2))  # 1 canal (mono)
                f.write(self.int_to_bytes(sample_rate))  # Fréquence d'échantillonnage
                f.write(self.int_to_bytes(sample_rate * 2))  # Byte rate
                f.write(self.int_to_bytes(2, 2))  # Alignement des blocs
                f.write(self.int_to_bytes(16, 2))  # Bits par échantillon
                
                # Chunk data
                f.write(b'data')
                f.write(self.int_to_bytes(data_size))  # Taille des données
                f.write(signal.tobytes())  # Écriture des données audio

            # Vérifier la sauvegarde
            if os.path.exists(filename) and os.path.getsize(filename) > 44:
                print(f"✅ Fichier {filename} sauvegardé avec succès.")
            else:
                print("❌ Erreur lors de la sauvegarde du fichier audio.")

        except Exception as e:
            print(f"❌ Erreur lors de l'écriture du fichier WAV: {e}")





# ---------------------- LANCEMENT DE L'APPLICATION ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioProcessorApp(root)
    root.mainloop()
