import datetime
milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000
# print(milliseconds_since_epoch)
# 1681504838876.137
# 1681491604701
epoch_start = 1681491604701
epoch_end = 1681491604701+86400000
epoch_end_timefmt = datetime.datetime.fromtimestamp(epoch_end/1000)
milliseconds_since_epoch_timefmt = datetime.datetime.fromtimestamp(
    milliseconds_since_epoch/1000)
time_remaining = epoch_end_timefmt - milliseconds_since_epoch_timefmt
epoch_time_remaining = epoch_end - milliseconds_since_epoch
print(time_remaining)
print(epoch_time_remaining)
