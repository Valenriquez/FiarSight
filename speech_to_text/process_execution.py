import subprocess

# Definir las rutas a los archivos Python
diarization_script = "diarization.py"
transcription_script = "transcription.py"
episode_text_script = "episode_text.py"

# Ejecutar diarization.py y esperar a que termine
print("Ejecutando diarization.py...")
subprocess.run(["python", diarization_script], check=True)
print("diarization.py completado.")

# Ejecutar transcription.py y esperar a que termine
print("Ejecutando transcription.py...")
subprocess.run(["python", transcription_script], check=True)
print("transcription.py completado.")

# Ejecutar episode_text.py y esperar a que termine
print("Ejecutando episode_text.py...")
subprocess.run(["python", episode_text_script], check=True)
print("episode_text.py completado.")
