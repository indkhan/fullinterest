"""YouTube service for fetching videos and transcripts."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for interacting with YouTube API and fetching transcripts."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize YouTube service with API key."""
        self.api_key = api_key or settings.YOUTUBE_API_KEY
        if not self.api_key:
            raise ValueError("YouTube API key is required")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def get_latest_videos_from_channel(
        self, 
        channel_id: str, 
        hours: int = 24,
        max_results: int = 50
    ) -> List[Dict]:
        """
        Get latest videos from a channel published within the last N hours.
        
        Args:
            channel_id: YouTube channel ID
            hours: Number of hours to look back (default: 24)
            max_results: Maximum number of results to return
            
        Returns:
            List of video dictionaries with metadata
        """
        try:
            # Calculate the time threshold (24 hours ago)
            time_threshold = datetime.utcnow() - timedelta(hours=hours)
            time_threshold_iso = time_threshold.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            # Get uploads playlist ID for the channel
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                logger.warning(f"Channel {channel_id} not found")
                return []
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from the uploads playlist
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                playlist_response = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                if not playlist_response.get('items'):
                    break
                
                # Get video IDs
                video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]
                
                # Get detailed video information
                videos_response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(video_ids)
                ).execute()
                
                for video in videos_response.get('items', []):
                    published_at = datetime.fromisoformat(
                        video['snippet']['publishedAt'].replace('Z', '+00:00')
                    )
                    
                    # Filter by time threshold
                    if published_at.replace(tzinfo=None) >= time_threshold:
                        video_data = {
                            'video_id': video['id'],
                            'title': video['snippet']['title'],
                            'description': video['snippet']['description'],
                            'channel_id': channel_id,
                            'channel_title': video['snippet']['channelTitle'],
                            'published_at': published_at.isoformat(),
                            'url': f"https://www.youtube.com/watch?v={video['id']}",
                            'thumbnail': video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                            'view_count': int(video['statistics'].get('viewCount', 0)),
                            'duration': video['contentDetails'].get('duration', ''),
                        }
                        videos.append(video_data)
                    else:
                        # Since videos are sorted by date, we can break early
                        break
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            logger.info(f"Found {len(videos)} videos from channel {channel_id} in the last {hours} hours")
            return videos[:max_results]
            
        except Exception as e:
            logger.error(f"Error fetching videos from channel {channel_id}: {str(e)}")
            return []
    
    def get_video_transcript(self, video_id: str, languages: List[str] = ['en']) -> Optional[str]:
        """
        Get transcript for a YouTube video.
        
        Args:
            video_id: YouTube video ID
            languages: List of language codes to try (default: ['en'])
            
        Returns:
            Transcript text as a single string, or None if not available
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get transcript in preferred languages
            transcript = None
            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    break
                except NoTranscriptFound:
                    continue
            
            # If no transcript in preferred languages, try to get any available
            if not transcript:
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                except:
                    # Try to get any available transcript
                    available = list(transcript_list)
                    if available:
                        transcript = available[0]
            
            if transcript:
                transcript_data = transcript.fetch()
                # Combine all transcript entries into a single text
                transcript_text = ' '.join([entry['text'] for entry in transcript_data])
                logger.info(f"Successfully fetched transcript for video {video_id}")
                return transcript_text
            else:
                logger.warning(f"No transcript available for video {video_id}")
                return None
                
        except TranscriptsDisabled:
            logger.warning(f"Transcripts are disabled for video {video_id}")
            return None
        except NoTranscriptFound:
            logger.warning(f"No transcript found for video {video_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching transcript for video {video_id}: {str(e)}")
            return None
    
    def get_videos_with_transcripts(
        self, 
        channel_ids: List[str], 
        hours: int = 24
    ) -> List[Dict]:
        """
        Get latest videos from multiple channels with their transcripts.
        
        Args:
            channel_ids: List of YouTube channel IDs
            hours: Number of hours to look back (default: 24)
            
        Returns:
            List of video dictionaries with transcripts included
        """
        all_videos = []
        
        for channel_id in channel_ids:
            logger.info(f"Fetching videos from channel: {channel_id}")
            videos = self.get_latest_videos_from_channel(channel_id, hours=hours)
            
            for video in videos:
                video_id = video['video_id']
                logger.info(f"Fetching transcript for video: {video['title']}")
                transcript = self.get_video_transcript(video_id)
                video['transcript'] = transcript
                all_videos.append(video)
        
        return all_videos

