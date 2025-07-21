from services.youtube_services import YouTubeService
from database.models import VideoModel
from utils.helpers import format_duration, display_video_list

def display_menu():
    print("\nYouTube Trend Analyzer")
    print("="*50)
    print("[1] Fetch Trending Videos")
    print("[2] Display Stored Videos")
    print("[3] Exit")
    print("="*50)
    return input("Please choose an option (1-3): ")

def validate_region_code(region_code):
    return len(region_code) == 2 and region_code.isalpha()

def fetch_videos():
    while True:  
        region_code = input("Please enter a region code (e.g., US, GB, JP): ").strip().upper()
        
        if not validate_region_code(region_code):
            print("Invalid region code. Please use 2 letter country codes (e.g., US, GB, JP)")
            continue  
        else:
            break  
    
    while True:  
        max_results = input("Please enter how many videos you want to fetch: ")
        
        try:
            max_results = int(max_results)
            if max_results <= 0:
                print("Please enter a positive number.")
                continue
            break  
        except ValueError:
            print("Please enter a valid number.")
            continue
    
    print(f"\nFetching {max_results} videos...")
    
    youtube_service = YouTubeService()
    video_model = VideoModel()
    
    try:
        trending_videos = youtube_service.get_trending_videos(region_code, max_results)
        
        if not trending_videos:
            print("No trending videos found.")
            return
        
        # Convert datetimes for display
        for video in trending_videos:
            _, display_datetime = video_model._convert_datetime(video['published_at'])
            video['display_published_at'] = display_datetime or video['published_at']
        
        display_video_list(
            trending_videos,
            title=f"Successfully fetched {len(trending_videos)} trending videos from region {region_code}"
        )
        
        # Insert to database
        inserted_count = video_model.insert_videos(trending_videos, region_code)
        
        if inserted_count > 0:
            print(f"\nSuccessfully stored {inserted_count} videos in database")
        else:
            print("\nNo videos were stored - possible database error")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        video_model.close()

def display_videos():
    video_model = None
    try:
        video_model = VideoModel()
        videos = video_model.get_all_videos()
        
        if not videos:
            print("\nNo videos found in database.")
            return
        
        # To group by region
        videos_by_region = {}
        for video in videos:
            region = video['region_code']
            if region not in videos_by_region:
                videos_by_region[region] = []
            videos_by_region[region].append(video)
        
        for region, region_videos in videos_by_region.items():
            display_video_list(
                region_videos,
                title=f"=== Videos from region: {region} ==="
            )
            
    except Exception as e:
        print(f"\nError retrieving videos: {e}")
    finally:
        if video_model:
            video_model.close()

def main():
    while True:
        choice = display_menu()
        
        if choice == '1':
            fetch_videos()
        elif choice == '2':
            display_videos()
        elif choice == '3':
            print("\nProgram exiting...")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()