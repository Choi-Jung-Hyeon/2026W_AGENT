#01_record_audio.py
import pyaudio
import wave
import os

# 녹음 설정
CHUNK = 1024  
FORMAT = pyaudio.paInt16 
CHANNELS = 1 
RATE = 16000
RECORD_SECONDS = 10 
OUTPUT_FILENAME = "Recode_ai/recorded_audio.wav"
INPUT_DEVICE_INDEX = 2   # 👈 위에서 찾은 번호로 변경!

os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

print("준비...")
audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=False,                  # ⭐ 중요
    input_device_index=INPUT_DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

print(f"{RECORD_SECONDS}초 녹음 시작!")

frames = []

for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)

print("녹음 완료!")

stream.stop_stream()
stream.close()
audio.terminate()

# WAV 파일로 저장
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"파일 저장 완료: {OUTPUT_FILENAME}")
