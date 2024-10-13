from youtube_transcript_api import YouTubeTranscriptApi
import csv

# Función para extraer el ID del video desde el link de YouTube
def get_video_id(youtube_url):
    return youtube_url.split("v=")[-1]

# Función para obtener la transcripción y guardarla en formato TSV
def obtener_transcripcion_tsv(youtube_url, idioma='en', output_file='yt_transcription.tsv'):
    video_id = get_video_id(youtube_url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[idioma])
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["start", "end", "text"])  # Encabezados
            for i in transcript:
                start_time = i['start']
                duration = i['duration']
                end_time = start_time + duration
                text = i['text']
                writer.writerow([start_time, end_time, text])
        print(f"Transcripción guardada en {output_file}")
    except Exception as e:
        print(f"No se pudo obtener la transcripción: {e}")

# Ejemplo de uso
youtube_url = 'https://www.youtube.com/watch?v=rLEhL8Y4SdU'
obtener_transcripcion_tsv(youtube_url)
