import csv
import json

# Función para cargar el archivo A (tsv)
def load_file_a(file_a):
    data_a = []
    with open(file_a, mode='r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            data_a.append({
                "start": int(row['start']),
                "end": int(row['end']),
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
                "speaker": row['SPEAKER'],
                "start": float(row['Start Time']),
                "end": float(row['End Time'])
            })
    return data_b

# Función para interpolar los intervalos huérfanos
def interpolate_speaker(file_a_data, file_b_data):
    results = []
    previous_speaker = None

    for i, b in enumerate(file_b_data):
        speaker_text = []
        if b['speaker'] == '':  # Si no tiene speaker asignado
            # Buscar speaker anterior y posterior
            previous_speaker = file_b_data[i-1]['speaker'] if i > 0 else None
            next_speaker = file_b_data[i+1]['speaker'] if i < len(file_b_data)-1 else None
            
            # Si el speaker anterior y posterior son iguales, asignar ese speaker
            if previous_speaker and next_speaker and previous_speaker == next_speaker:
                b['speaker'] = previous_speaker
            elif previous_speaker:  # Si solo hay speaker anterior, asignar ese
                b['speaker'] = previous_speaker
            elif next_speaker:  # Si solo hay speaker posterior, asignar ese
                b['speaker'] = next_speaker

        # Agregar el texto para el speaker encontrado
        for a in file_a_data:
            a_start_seconds = a['start'] / 1000.0
            a_end_seconds = a['end'] / 1000.0
            if a_start_seconds < b['end'] and a_end_seconds > b['start']:
                speaker_text.append(a['text'])
        
        concatenated_text = " ".join(speaker_text)
        results.append({
            "speaker": b['speaker'],
            "start_time": b['start'],
            "end_time": b['end'],
            "text": concatenated_text
        })
    
    return results

# Guardar el resultado como un archivo JSON
def save_to_json(data, output_file):
    with open(output_file, mode='w') as file:
        json.dump(data, file, indent=4)

# Rutas de los archivos
file_a = "debate_1.tsv"  # Asegúrate de que sea la ruta correcta del archivo A (TSV)
file_b = "compressed_diarization_output.csv"  # Asegúrate de que sea la ruta correcta del archivo B (CSV)
output_file = "output.json"

# Cargar los datos de ambos archivos
file_a_data = load_file_a(file_a)
file_b_data = load_file_b(file_b)

# Interpolar y asignar los intervalos huérfanos
result_data = interpolate_speaker(file_a_data, file_b_data)

# Guardar el resultado como JSON
save_to_json(result_data, output_file)

print(f"Archivo JSON interpolado guardado como {output_file}")
