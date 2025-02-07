from crontab import CronTab
import sys
import os

python_bin = sys.executable

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
website_build_command = "cp -f prices.csv /var/www/hgpereira/static/  && cd /var/www/hgpereira && sudo hugo -b https://www.hgpereira.com"

if not os.access(script_path, os.X_OK):
    os.chmod(script_path, 0o755)

cron = CronTab(user=True)

update_jobs = [
    ('0 9-23 * * 5', 'Sexta Feira -- Verifica se saiu post'),
    ('0 * * * 6', 'Sabado -- Verifica se saiu post'),
    ('0 0-9 * * 7', 'Domigo -- Verifica se saiu post'),
]

for schedule, comment in update_jobs:
    update_job = cron.new(command=f'{python_bin} {script_path}', comment=comment)
    update_job.setall(schedule)

    minute, hour, day, month, weekday = schedule.split(" ")

    if minute.isdigit():
        new_minute = (int(minute) + 5) % 60
    else:
        new_minute = minute  # Keep it unchanged if it's '*', a range, or a list

    if minute.isdigit() and int(minute) + 5 >= 60:
        if hour.isdigit():
            new_hour = str(int(hour) + 1)
        else:
            new_hour = hour
    else:
        new_hour = hour

    new_schedule = f"{new_minute} {new_hour} {day} {month} {weekday}"

    build_job = cron.new(command=website_build_command, comment=f'Copy file after {comment}')
    build_job.setall(new_schedule)

cron.write()

for j in cron:
    print(f"Added: {j.comment} - {j}")
