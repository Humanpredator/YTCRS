from datetime import datetime, timedelta

from apscheduler.jobstores.base import JobLookupError
from cachetools import func
import pytz

from server import scheduler, LOGGER


def datetime_india():
    datetime_str = datetime.now(pytz.timezone(
        'Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S.%f")
    datetime_obj = datetime.strptime(str(datetime_str), "%Y-%m-%d %H:%M:%S.%f")

    return datetime_obj


def add_scheduler(function: func, start_time=None, end_time=None, interval=None, start_date=None, end_date=None):
    # Set default values using a dictionary
    defaults = {
        'start_date': datetime.now().strftime("%Y-%m-%d"),
        'end_date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        'start_time': "00:00",
        'end_time': "23:59",
        'interval': 60 * 24 if end_date is None else None
    }

    # Update the defaults with the provided values
    start_date, end_date, start_time, end_time, interval = (
        value if value is not None else defaults[key]
        for key, value in zip(defaults.keys(), (start_date, end_date, start_time, end_time, interval))
    )

    # Use pytz timezone to get the timezone with PEP 495 support
    tz = pytz.timezone('asia/kolkata')

    start_datetime = tz.localize(datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M"))
    end_datetime = tz.localize(datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M"))

    job_id = f"{function.__name__}()_job"

    # Remove the existing job if it exists
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        pass  # Job doesn't exist, proceed to add it
    delay = (start_datetime - datetime.now(tz)).total_seconds()
    scheduler.add_job(function, 'interval', minutes=interval,
                      start_date=start_datetime + timedelta(seconds=delay), end_date=end_datetime, id=job_id)
    LOGGER.info(f"Function {function.__name__}() was added to Scheduler with job ID: {job_id} ...!")
