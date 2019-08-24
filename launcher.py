import subprocess
import os

python_dir = '/home/pi/rocket/venv/bin/python3'
process_dir = '/home/pi/rocket/modules'

for filename in [name for name in os.listdir(process_dir) if os.path.isfile(os.path.join(process_dir, name)) and name.endswith('.py')]:
    subprocess.Popen([python_dir, os.path.join(process_dir, filename)])

