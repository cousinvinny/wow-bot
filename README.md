1. git clone https://github.com/cousinvinny/wow-bot (to a folder on desktop)
2. make a bash script:

#!/bin/bash
source /home/vinh/Desktop/wow_discord_bot/venv/bin/activate
python3 /home/vinh/Desktop/wow_discord_bot/main.py

3. Make a cronjob to execute the bash script every hour

0 * * * * bash /home/vinh/Desktop/wow_discord_bot/task.sh
