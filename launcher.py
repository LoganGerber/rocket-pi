import subprocess
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
python_dir = os.path.join(script_dir, 'venv/bin/python3')
process_dir = os.path.join(script_dir, 'modules')

for filename in [name for name in os.listdir(process_dir) if os.path.isfile(os.path.join(process_dir, name)) and name.endswith('.py')]:
    subprocess.Popen([python_dir, os.path.join(process_dir, filename)])

