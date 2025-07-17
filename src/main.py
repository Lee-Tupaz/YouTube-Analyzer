from services.youtube_services import YouTubeService
from database.models import VideoModel
from utils.helpers import print_video_info

def display_menu():
    print("\nYouTube Trend Analyzer")
    print("="*50)
    print("[1] Fetch Trending Videos")
    print("[2] Display Stored Videos")
    print("[3] Exit")
    print("="*50)
    return input("Please choose an option (1-3): ")

def fetch_videos():
    region_code = input("Please enter a region code (e.g., US, GB, JP): ").strip().upper()
    max_results = input("Please enter how many videos you want to fetch: ")
    
    try:
        max_results = int(max_results)
        if max_results <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    print(f"\nFetching {max_results} videos...")
    
    youtube_service = YouTubeService()
    video_model = VideoModel()
    
    try:
        trending_videos = youtube_service.get_trending_videos(region_code, max_results)
        
        if not trending_videos:
            print("No trending videos found.")
            return
        
        print(f"\nSuccessfully fetched {len(trending_videos)} trending videos from region {region_code}")
        
        for i, video in enumerate(trending_videos, 1): 
            print(f"\nVideo {i}:")
            print_video_info(video)
            print("-" * 50) 
        
        inserted_count = video_model.insert_videos(trending_videos, region_code)
        
        if inserted_count > 0:
            print(f"\nSuccessfully stored {inserted_count} videos in database.")
        else:
            print("\nNo videos were stored. Possible database error.")
            
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
            
        print(f"\nFound {len(videos)} videos in database:")
        print("-" * 70)
        
        for i, video in enumerate(videos, 1):
            print(f"\nVideo {i} (Displaying trending videos in region: {video['region_code']}):")
            print_video_info(video)
            print("-" * 70)
            
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