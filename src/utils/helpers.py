def format_duration(duration):
    duration = duration.replace('PT', '')
    
    hours = 0
    if 'H' in duration:
        hours_part = duration.split('H')[0]
        hours = int(hours_part)
        duration = duration.split('H')[1]
    
    minutes = 0
    if 'M' in duration:
        minutes_part = duration.split('M')[0]
        minutes = int(minutes_part)
        duration = duration.split('M')[1]
    
    seconds = 0
    if 'S' in duration:
        seconds_part = duration.split('S')[0]
        seconds = int(seconds_part)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def print_video_info(video):
    # Use the display format if available, fallback to original
    published_at = video.get('display_published_at', video['published_at'])
    
    print(f"Title: {video['title']}")
    print(f"Channel: {video['channel_title']}")
    print(f"Published: {video['display_published_at']}")
    print(f"Views: {video['view_count']:,}")
    print(f"Likes: {video['like_count']:,}")
    print(f"Comments: {video['comment_count']:,}")
    print(f"Duration: {format_duration(video['duration'])}")