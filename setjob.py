from crontab import CronTab
import sys
import os

python_bin = sys.executable

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

if not os.access(script_path, os.X_OK):
    os.chmod(script_path, 0o755)

cron = CronTab(user=True)
job = cron.new(command=f'{python_bin} {script_path}', comment='Updates nos Precos dos Combustiveis')

job.setall('0 20 * * 5')

cron.write()

print(f"Added: {job}")
