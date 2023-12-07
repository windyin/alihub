from . import __xmltv
from epg.model import Channel, Program
from datetime import datetime, date, timedelta, timezone


def update(channel: Channel, scraper_params: str, dt: date = datetime.today().date()) -> bool:
    if scraper_params.find('@http') == -1:
        scraper_url = scraper_params
    else:
        scraper_id = scraper_params.split('@http', 1)[0]
        scraper_url = "http" + scraper_params.split('@http', 1)[1]
    channel_id = channel.id if scraper_id == None else scraper_id
    scraper_channels = __xmltv.get_channels(scraper_url)
    found_channel = False

    for scraper_channel in scraper_channels:        
        if scraper_channel.id == channel_id:
            
            found_channel = True
            channel.flush(dt)
            for program in scraper_channel.programs:
                start_time_tz = program.start_time.astimezone(timezone(timedelta(hours=8)))
                start_time = program.start_time
                
                #if start_time.date() != dt:
                if start_time_tz.date() != dt:                    
                    continue
                end_time = program.end_time                
                title = program.title
                # Purge channel programs on this date
                #channel.flush(dt)
                # Update channel programs on this date
                desc = program.desc if program.desc is not None else ''
                channel.programs.append(Program(title, start_time, end_time, channel.id, desc))                
                #print(program.title + " " + program.start_time.strftime("%Y-%m-%d %H:%M:%S %Z") + " - " + end_time.strftime("%Y-%m-%d %H:%M:%S %Z"))                
            channel.metadata.update({'last_update': datetime.now(timezone.utc).astimezone()})
        #return True
    return found_channel
