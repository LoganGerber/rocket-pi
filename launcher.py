import subprocess
import os

python_dir = '/home/pi/rocket/venv/bin/python3'
process_dir = '/home/pi/rocket/processes'

for filename in [name for name in os.listdir(process_dir) if os.path.isfile(os.path.join(process_dir, name))]:
    subprocess.Popen([python_dir, os.path.join(process_dir, filename)])

