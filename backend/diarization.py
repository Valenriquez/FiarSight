import csv
import os
from pyannote.audio import Pipeline

def find_audio_file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    project_dir = os.path.dirname(parent_dir)

    possible_paths = [
        os.path.join(current_dir, "audio", filename),
        os.path.join(parent_dir, "audio", filename),
        os.path.join(project_dir, "audio", filename),
        os.path.join(project_dir, filename)
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    print("Searched in the following locations:")
    for path in possible_paths:
        print(f"- {path}")
    raise FileNotFoundError(f"The audio file {filename} was not found in any of the expected locations.")

# Try to find the audio file
audio_filename = "debate_1.wav"
try:
    audio_file = find_audio_file(audio_filename)
    print(f"Found audio file at: {audio_file}")
except FileNotFoundError as e:
    print(e)
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of the current directory:")
    print(os.listdir(os.getcwd()))
    raise

# Initialize the pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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"
)

# Perform diarization
print(f"Performing diarization on {audio_file}")
diarization = pipeline(audio_file)

# Nombre del archivo CSV de salida
csv_filename = "compressed_diarization_output.csv"

# Crear lista para almacenar los intervalos comprimidos
compressed_diarization = []

# Inicializar variables para almacenar el speaker actual y su intervalo
current_speaker = None
current_start = None
current_end = None

# Recorrer los resultados de la diarización
for turn, _, speaker in diarization.itertracks(yield_label=True):
    if speaker == current_speaker:
        # Si el mismo speaker continúa, actualiza el final del intervalo
        current_end = turn.end
    else:
        # Si el speaker cambia, guarda el intervalo anterior
        if current_speaker is not None:
            compressed_diarization.append([f"{current_speaker}", current_start, current_end])
        # Actualizar al nuevo speaker y su intervalo
        current_speaker = speaker
        current_start = turn.start
        current_end = turn.end

# Añadir el último intervalo si existe
if current_speaker is not None:
    compressed_diarization.append([f"{current_speaker}", current_start, current_end])

# Guardar los intervalos comprimidos en el archivo CSV
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Escribir la cabecera
    writer.writerow(["Speaker", "Start Time", "End Time"])

    # Escribir los datos comprimidos
    writer.writerows(compressed_diarization)

print(f"Archivo CSV comprimido guardado como {csv_filename}")
