"""Layanan ML (Model Loading & Inference) dengan sistem cache Streamlit."""

import gc
import torch
import streamlit as st

try:
    from transformers import AutoFeatureExtractor as FeatureExtractor
except ImportError:
    try:
        from transformers import Wav2Vec2FeatureExtractor as FeatureExtractor
    except ImportError:
        from transformers.models.wav2vec2.feature_extraction_wav2vec2 import Wav2Vec2FeatureExtractor as FeatureExtractor

from model import load_model
from utils import load_audio, preprocess_audio, predict_emotion
from config import SER_BACKBONE


@st.cache_resource(show_spinner="Memuat model WavLM...")
def load_ser_model(device_name: str):
    device = torch.device(device_name)
    model = load_model(device=device)
    return model, device


@st.cache_resource(show_spinner="Memuat feature extractor...")
def load_feature_extractor():
    return FeatureExtractor.from_pretrained(SER_BACKBONE)


@st.cache_resource(show_spinner="Memuat Whisper (STT)...")
def load_whisper_lazy(model_name: str, device_name: str):
    """Cache pipeline Whisper — hanya dimuat saat user pertama kali minta transkrip."""
    from utils import create_whisper_pipeline
    return create_whisper_pipeline(model_name, device_name)


def check_model_ready(device_name: str) -> tuple[bool, str | None]:
    try:
        load_ser_model(device_name)
        load_feature_extractor()
        return True, None
    except FileNotFoundError as exc:
        return False, str(exc)
    except RuntimeError as exc:
        return False, str(exc)
    except Exception as exc:
        return False, f"Gagal memuat model: {exc}"


def run_prediction(uploaded_file, device_name: str) -> tuple[dict, dict]:
    with st.spinner("Menganalisis pola emosi dari audio..."):
        model, device = load_ser_model(device_name)
        processor = load_feature_extractor()
        uploaded_file.seek(0)
        waveform, sample_rate = load_audio(uploaded_file)
        processed_waveform, preprocess_info = preprocess_audio(waveform, sample_rate)
        result = predict_emotion(model, processor, processed_waveform, device)
        gc.collect()
    return result, preprocess_info
