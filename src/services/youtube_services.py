from googleapiclient.discovery import build
from config.settings import youtube_api_key

class YouTubeService:
    
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    def get_trending_videos(self, region_code, max_results):
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=max_results
            )
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_data = {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'description': item['snippet']['description'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'comment_count': int(item['statistics'].get('commentCount', 0)),
                    'duration': item['contentDetails']['duration'],
                    'category_id': int(item['snippet']['categoryId']),
                    'tags': item['snippet'].get('tags', [])
                }
                videos.append(video_data)
            
            return videos
        except Exception as e:
            print(f"Error fetching trending videos: {e}")
            return []