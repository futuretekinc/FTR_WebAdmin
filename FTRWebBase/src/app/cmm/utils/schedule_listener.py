
# http://apscheduler.readthedocs.io/en/3.0/modules/events.html?highlight=event_job_executed
from apscheduler.events import EVENT_JOB_EXECUTED,EVENT_JOB_ERROR

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print("=======================================")
        print(event.job_id)
        print(event.alias)
        print(event.code)
        print(event.jobstore)
        print(event.scheduled_run_time)
        print(event.traceback)
        print('The job worked :)')
        print("=======================================")
'''
if __name__ == '__main__':
    app = create_app(SQLITE3)
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.init_app(app)
    scheduler.start()

    app.run()



'''