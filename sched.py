import os, time, schedule

def job():
    os.system('python3 ManAge_Wrapper.py')

schedule.every().friday.at('23:05').do(job)

while True:
    schedule.run_pending()
    time.sleep(1)