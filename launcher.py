import subprocess
import os

python_dir = '/home/pi/rocket/venv/bin/python3'
process_dir = '/home/pi/rocket/processes'

launched_count = 0

for filename in [name for name in os.listdir(process_dir) if os.path.isfile(os.path.join(process_dir, name)) and name.endswith('.py')]:
    subprocess.Popen([python_dir, os.path.join(process_dir, filename)])
    launched_count += 1

print(launched_count)

