import subprocess
import sys
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the Python files
diarization_script = os.path.join(current_dir, "diarization.py")
transcription_script = os.path.join(current_dir, "transcription.py")
episode_text_script = os.path.join(current_dir, "episode_text.py")

# Use the same Python interpreter that's running this script
python_executable = sys.executable

def run_script(script_name, script_path):
    print(f"Ejecutando {script_name}...")
    try:
        subprocess.run([python_executable, script_path], check=True)
        print(f"{script_name} completado.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")
        sys.exit(1)

run_script("diarization.py", diarization_script)
run_script("transcription.py", transcription_script)
run_script("episode_text.py", episode_text_script)
