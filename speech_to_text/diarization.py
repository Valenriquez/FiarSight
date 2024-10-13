import csv
from pyannote.audio import Pipeline

# Cargar el pipeline preentrenado sin cambiar el dispositivo (por defecto usará CPU)
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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"
)

# Aplicar el pipeline preentrenado al archivo de audio
diarization = pipeline("audio/debate_1.wav")

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
