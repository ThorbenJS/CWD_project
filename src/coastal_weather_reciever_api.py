import datetime as dt
from datetime import timezone
from fmiopendata.wfs import download_stored_query


end_time = dt.datetime.now(timezone.utc)
start_time = end_time - dt.timedelta(minutes=5)

start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")


observation = download_stored_query(
    "fmi::observations::weather::multipointcoverage",
    args=[
        "fmisid=100947",
        "starttime=" + start_time,
        "endtime=" + end_time
        ]
)


print(observation.data.keys())

latest_observation = max(observation.data.keys())

