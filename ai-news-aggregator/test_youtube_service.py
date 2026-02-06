"""Test script for YouTube service."""
import os
import logging
from dotenv import load_dotenv
from app.services.youtube_service import YouTubeService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()


def main():
    """Test YouTube service with sample channel IDs."""
    
    # Check if API key is set
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("ERROR: YOUTUBE_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return
    
    # Initialize service
    try:
        youtube_service = YouTubeService(api_key=api_key)
        print("✓ YouTube service initialized successfully\n")
    except Exception as e:
        print(f"ERROR: Failed to initialize YouTube service: {e}")
        return
    
    # Example channel IDs - replace with your own
    # You can find channel IDs from YouTube channel URLs or use channel usernames
    channel_ids = [
        "UCgfe2ooZD3VJPB6aJAnuQng",
    ]
    
    if not channel_ids:
        print("No channel IDs specified. Please add channel IDs to test.")
        print("\nTo find a channel ID:")
        print("1. Go to the YouTube channel page")
        print("2. View page source (Ctrl+U)")
        print("3. Search for 'channelId' or check the URL")
        print("4. Or use a tool like: https://commentpicker.com/youtube-channel-id.php")
        return
    
    print(f"Testing with {len(channel_ids)} channel(s)...\n")
    print("=" * 80)
    
    # Get videos from last 24 hours with transcripts
    videos = youtube_service.get_videos_with_transcripts(
        channel_ids=channel_ids,
        hours=24
    )
    
    if not videos:
        print("\nNo videos found in the last 24 hours from the specified channels.")
        return
    
    print(f"\n✓ Found {len(videos)} video(s) in the last 24 hours\n")
    print("=" * 80)
    
    # Display results
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}] {video['title']}")
        print(f"    Channel: {video['channel_title']}")
        print(f"    Published: {video['published_at']}")
        print(f"    URL: {video['url']}")
        print(f"    Views: {video['view_count']:,}")
        
        if video.get('transcript'):
            transcript_preview = video['transcript'][:200] + "..." if len(video['transcript']) > 200 else video['transcript']
            print(f"    Transcript: {transcript_preview}")
            print(f"    Transcript length: {len(video['transcript'])} characters")
        else:
            print(f"    Transcript: Not available")
        
        print("-" * 80)


if __name__ == "__main__":
    main()

