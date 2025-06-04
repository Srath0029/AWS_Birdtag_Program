# test_preprocess_audio.py

from lamda.inference.audio_preprocessing import preprocess_audio
from lamda.inference.model_runner import BirdNetRunner
import matplotlib.pyplot as plt
import numpy as np
import time
import traceback

AUDIO_PATH = "sample_audio.wav"  # ← place your .wav file here

def main():
    print("🐣 BirdTag Model Debug Session Start")

    try:
        print("🔄 [1/3] Preprocessing audio...")
        start_time = time.time()
        mel = preprocess_audio(AUDIO_PATH)
        print(f"✅ Spectrogram shape: {mel.shape}")
        print(f"   Min: {np.min(mel):.4f}, Max: {np.max(mel):.4f}")
        print(f"⏱️ Took {time.time() - start_time:.2f} seconds")

        
        print("🧠 [2/3] Running model inference...")
        runner = BirdNetRunner()

        start_time = time.time()
        predictions = runner.predict(mel, top_k=5)
        print(f"✅ Model inference completed in {time.time() - start_time:.2f} seconds")

        print("\n🎯 [3/3] Top Predictions:")
        for result in predictions:
            print(f"   - {result['label']}: {result['confidence']:.4f}")

    except Exception as e:
        print("❌ An error occurred during execution:")
        traceback.print_exc()

    print("🏁 Script execution finished.")

if __name__ == "__main__":
    main()
