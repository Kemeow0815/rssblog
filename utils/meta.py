from datetime import datetime
from pytz import timezone

def meta():
    DATE = datetime.now(tz=timezone('Asia/Shanghai'))
    UPTIME = DATE.isoformat(timespec='seconds')
    TODAY = DATE.strftime('%Y-%m-%d')
    
    mt = {
        'timestamp': DATE.timestamp(),
        'updatetime': UPTIME,
        'today': TODAY
    }

    return mt
