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

# Función para encontrar y concatenar el texto correspondiente, sin excluir ningún registro
def match_speaker_with_text(file_a_data, file_b_data):
    results = []
    for b in file_b_data:
        speaker_text = []
        # Buscar todas las frases de A que se solapan con el intervalo de B
        for a in file_a_data:
            # Convertir los tiempos de A de milisegundos a segundos para compararlos con los tiempos de B
            a_start_seconds = a['start'] / 1000.0
            a_end_seconds = a['end'] / 1000.0
            
            # Verificar si el registro A se solapa con el intervalo de B
            if (a_start_seconds < b['end'] and a_end_seconds > b['start']):
                speaker_text.append(a['text'])
        
        # Concatenar todas las frases y agregar el resultado
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

# Encontrar el texto correspondiente para cada speaker en el archivo B
result_data = match_speaker_with_text(file_a_data, file_b_data)

# Guardar el resultado como JSON
save_to_json(result_data, output_file)

print(f"Archivo JSON guardado como {output_file}")
