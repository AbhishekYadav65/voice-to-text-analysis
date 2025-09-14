# backend/pipeline/preprocess.py
import os
import shutil
from pathlib import Path

def clean_audio(input_path: str) -> str:
    """
    Basic passthrough + optional format conversion placeholder.
    Return: path to audio file (same input for now).
    Replace this function with denoising / amplification as needed.
    """
    # placeholder: just return input
    return input_path
