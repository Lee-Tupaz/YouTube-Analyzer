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
    
def display_video_list(videos, title=None):
    
    if not videos:
        print("No videos to display")
        return
    
    if title:
        print(f"\n{title}")
        print("-" * 70)
    
    for i, video in enumerate(videos, 1):
        print(f"\nVideo {i}:")
        print("=" * 50)
        print(f"Title: {video['title']}")
        print(f"Channel: {video['channel_title']}")
        print(f"Published: {video['display_published_at']}")
        print(f"Views: {video['view_count']:,}")
        print(f"Likes: {video['like_count']:,}")
        print(f"Comments: {video['comment_count']:,}")
        print(f"Duration: {format_duration(video['duration'])}")
        print(f"URL: {video['youtube_url']}")
        print("=" * 50)