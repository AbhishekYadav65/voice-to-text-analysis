import librosa
import soundfile as sf
import numpy as np
from scipy import signal
import os

def clean_audio(file_path: str) -> str:
    """
    Enhanced audio preprocessing for Whispering Shadows Mystery.
    Handles trembling whispers, static interference, background noise, and volume variations.
    Returns path to cleaned audio file.
    """
    try:
        # Load audio with librosa (handles various formats)
        y, sr = librosa.load(file_path, sr=None)
        
        # 1. Remove DC offset
        y = y - np.mean(y)
        
        # 2. Normalize volume (handle whispers and shouts)
        y = librosa.util.normalize(y)
        
        # 3. Reduce background noise using spectral gating
        y = reduce_background_noise(y, sr)
        
        # 4. Enhance speech clarity
        y = enhance_speech(y, sr)
        
        # 5. Remove static and clicks
        y = remove_static(y, sr)
        
        # 6. Final normalization
        y = librosa.util.normalize(y)
        
        # Save cleaned audio
        output_path = file_path.replace('.', '_cleaned.')
        sf.write(output_path, y, sr)
        
        return output_path
        
    except Exception as e:
        print(f"Error in audio preprocessing: {e}")
        return file_path  # Return original if cleaning fails

def reduce_background_noise(y, sr, noise_reduce_factor=0.8):
    """Reduce background noise using spectral subtraction"""
    # Compute STFT
    stft = librosa.stft(y)
    magnitude = np.abs(stft)
    phase = np.angle(stft)
    
    # Estimate noise from quiet parts
    noise_floor = np.percentile(magnitude, 20, axis=1, keepdims=True)
    
    # Apply spectral subtraction
    enhanced_magnitude = magnitude - noise_reduce_factor * noise_floor
    enhanced_magnitude = np.maximum(enhanced_magnitude, 0.1 * magnitude)
    
    # Reconstruct signal
    enhanced_stft = enhanced_magnitude * np.exp(1j * phase)
    return librosa.istft(enhanced_stft)

def enhance_speech(y, sr):
    """Enhance speech frequencies (300-3400 Hz)"""
    # Design bandpass filter for speech frequencies
    nyquist = sr / 2
    low = 300 / nyquist
    high = 3400 / nyquist
    
    b, a = signal.butter(4, [low, high], btype='band')
    return signal.filtfilt(b, a, y)

def remove_static(y, sr):
    """Remove static and clicks using median filtering"""
    # Apply median filter to remove spikes/static
    window_size = int(0.01 * sr)  # 10ms window
    if window_size % 2 == 0:
        window_size += 1
    
    return signal.medfilt(y, kernel_size=window_size)

