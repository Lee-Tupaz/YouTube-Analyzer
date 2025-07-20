from datetime import datetime
from database.db_connector import DatabaseConnector

class VideoModel:
    def __init__(self):
        self.db = DatabaseConnector()
        if not self.db.connect():
            raise Exception("Failed to connect to database")
        self._create_tables()
    
    def _create_tables(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS trending_videos (
            id VARCHAR(255) PRIMARY KEY,
            title TEXT NOT NULL,
            channel_title TEXT NOT NULL,
            published_at DATETIME NOT NULL,
            display_published_at TEXT,
            description TEXT,
            thumbnail_url TEXT,
            view_count INT,
            like_count INT,
            comment_count INT,
            duration TEXT,
            category_id INT,
            tags TEXT,
            region_code VARCHAR(10) NOT NULL,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        if not self.db.execute_query(create_table_query):
            raise Exception("Failed to create tables")
    
    def _convert_datetime(self, iso_datetime):
        try:
            dt = datetime.strptime(iso_datetime, "%Y-%m-%dT%H:%M:%SZ")
            mysql_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
            display_datetime = dt.strftime("%B %d, %Y - %I:%M %p")
            return mysql_datetime, display_datetime
        except (ValueError, TypeError):
            return None,None
    
    def insert_videos(self, videos_data, region_code):
        if not videos_data:
            return 0
        
        query = """
        INSERT INTO trending_videos (
        id, title, channel_title, published_at, description, 
        thumbnail_url, view_count, like_count, comment_count, 
        duration, category_id, tags, region_code, display_published_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            view_count = VALUES(view_count),
            like_count = VALUES(like_count),
            comment_count = VALUES(comment_count),
            display_published_at = VALUES(display_published_at)
        """
        
        params_list = []
        for video_data in videos_data:
            mysql_datetime, display_datetime = self._convert_datetime(video_data['published_at'])
            if not mysql_datetime:
                continue
                
            tags = ",".join(video_data.get('tags', [])) if 'tags' in video_data else ""
            
            params = (
                video_data['id'],
                video_data['title'],
                video_data['channel_title'],
                mysql_datetime,
                video_data.get('description', ''),
                video_data.get('thumbnail_url', ''),
                video_data.get('view_count', 0),
                video_data.get('like_count', 0),
                video_data.get('comment_count', 0),
                video_data.get('duration', ''),
                video_data.get('category_id', 0),
                tags,
                region_code,
                display_datetime
            )
            params_list.append(params)
        
        try:
            cursor = self.db.connection.cursor()
            cursor.executemany(query, params_list)
            self.db.connection.commit()
            row_count = len(params_list)
            cursor.close()
            return row_count
        except Exception as e:
            print(f"Error inserting videos: {e}")
            self.db.connection.rollback()
            return 0
    
    def get_all_videos(self):
        query = "SELECT * FROM trending_videos ORDER BY region_code, fetched_at DESC"
        result = self.db.execute_query(query, fetch=True)
        return result if result else []
    
    def close(self):
        self.db.disconnect()