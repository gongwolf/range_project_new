from datetime import datetime
from pathlib import Path
import json

log_folder = "Z:\logs"
p = Path(log_folder)
test_file = p/"test.txt"

with open(test_file, 'w') as f:
    f.write('This is a test of \n')
    f.write('writing someting into the network drive \n')
    f.write(datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f"))