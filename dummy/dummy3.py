import pyaudio
p = pyaudio.PyAudio()

print("사용 가능한 오디오 장치 목록:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(
        f"{i}: {info['name']} | "
        f"Input={info['maxInputChannels']} | "
        f"Output={info['maxOutputChannels']}"
    )

p.terminate()
