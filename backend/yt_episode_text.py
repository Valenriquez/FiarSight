import csv
import json

# Función para cargar el archivo A (tsv)
def load_file_a(file_a):
    data_a = []
    with open(file_a, mode='r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            data_a.append({
                "start": float(row['start']),
                "end": float(row['end']),
                "text": row['text']
            })
    return data_a

# Función para cargar el archivo B (csv)
def load_file_b(file_b):
    data_b = []
    with open(file_b, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_b.append({
                "speaker": row['Speaker'],
                "start": float(row['Start Time']),
                "end": float(row['End Time'])
            })
    return data_b

# Función con two-pointers para evitar duplicación y procesar eficientemente
def match_speaker_with_text_two_pointers(file_a_data, file_b_data):
    results = []
    a_idx = 0
    b_idx = 0

    while b_idx < len(file_b_data):
        b = file_b_data[b_idx]
        speaker_text = []
        
        # Usamos el puntero a_idx para procesar los textos de A
        while a_idx < len(file_a_data):
            a = file_a_data[a_idx]
            a_start_seconds = a['start']
            a_end_seconds = a['end']

            # Verificar si hay solapamiento entre A y B
            if a_end_seconds < b['start']:
                # Si A termina antes de que B empiece, avanzamos en A
                a_idx += 1
            elif a_start_seconds > b['end']:
                # Si A empieza después de que B termina, dejamos de procesar A para este B
                break
            else:
                # Hay solapamiento, añadimos el texto
                speaker_text.append(a['text'])
                a_idx += 1

        # Concatenar el texto del speaker actual
        concatenated_text = " ".join(speaker_text)

        # Si no tiene speaker asignado, interpolar usando el contexto
        if b['speaker'] == '':
            previous_speaker = file_b_data[b_idx-1]['speaker'] if b_idx > 0 else None
            next_speaker = file_b_data[b_idx+1]['speaker'] if b_idx < len(file_b_data)-1 else None
            if previous_speaker and next_speaker and previous_speaker == next_speaker:
                b['speaker'] = previous_speaker
            elif previous_speaker:
                b['speaker'] = previous_speaker
            elif next_speaker:
                b['speaker'] = next_speaker

        # Agregar los datos al resultado final
        if concatenated_text.strip() != '':
            results.append({
                "speaker": b['speaker'],
                "start_time": b['start'],
                "end_time": b['end'],
                "text": concatenated_text
            })

        # Avanzar en B
        b_idx += 1

    return results

# Guardar el resultado como un archivo JSON
def save_to_json(data, output_file):
    with open(output_file, mode='w') as file:
        json.dump(data, file, indent=4)

# Rutas de los archivos
file_a = "yt_transcription.tsv"  # Asegúrate de que sea la ruta correcta del archivo A (TSV)
file_b = "compressed_diarization_output.csv"  # Asegúrate de que sea la ruta correcta del archivo B (CSV)
output_file = "yt_time_line.json"

# Cargar los datos de ambos archivos
file_a_data = load_file_a(file_a)
file_b_data = load_file_b(file_b)

# Encontrar el texto correspondiente para cada speaker en el archivo B
result_data = match_speaker_with_text_two_pointers(file_a_data, file_b_data)

# Guardar el resultado como JSON
save_to_json(result_data, output_file)

print(f"Archivo JSON refinado con two-pointers guardado como {output_file}")
