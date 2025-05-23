import sched, time
import datetime

s = sched.scheduler(time.time, time.sleep)
def print_time( a = 'default' ):
    print("From print_time", time.time(), a)

def calc_time( h = 0, m = 0, s = 0 , ms = 0 ):
    """Calculate the epoch timestamp for today's date at the given time."""
    now = datetime.datetime.now()
    dt = datetime.datetime( year = now.year, month = now.month, day = now.day, hour = h, minute = m, second = s , microsecond = ms )
    return int( dt.timestamp() )


def print_some_times():
#    print(time.time())
    workday_starttime = calc_time( 7 , 10 , 0 )
#    print( workday_starttime )
    s.enter(1, 1, print_time)
    s.enter(2, 2, print_time, argument=('positional',))
    # despite having higher priority, 'keyword' runs after 'positional' as enter() is relative
    s.enter(3, 3, print_time, kwargs={'a': 'keyword'})
    s.enterabs( calc_time( 7 , 14 , 0 ) , 0, print_time, argument=("first enterabs",))
    s.enterabs( calc_time( 7 , 14 , 30 ) , 0, print_time, argument=("second enterabs",))
    s.run()
#    print(time.time())

print_some_times()