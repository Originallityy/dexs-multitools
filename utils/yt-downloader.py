import os
import sys
import re
import subprocess
import shutil
from urllib.parse import urlparse, parse_qs
import inquirer

def extract_video_id(url):
    """Extract the YouTube video ID from various URL formats"""
    print(f"Extracting ID from URL: {url}")
    
    # YouTube URL parsing
    if 'youtube.com' in url or 'youtu.be' in url:
        # Handle youtu.be links
        if 'youtu.be' in url:
            parts = url.split('/')
            for part in parts:
                if 'youtu.be' not in part and len(part) == 11:
                    return part
                    
        # Handle standard youtube.com links
        if 'v=' in url:
            video_id = url.split('v=')[1]
            if '&' in video_id:
                video_id = video_id.split('&')[0]
            return video_id
    
    print(f"Could not extract video ID, using URL as identifier")
    # Generate a simple hash of the URL if we can't extract ID
    return str(abs(hash(url)) % (10 ** 10))

def simple_download(url, user):
    """Basic download function that avoids fetching metadata"""
    try:
        # Extract video ID or generate hash from URL
        video_id = extract_video_id(url)
        
        # Create directory structure
        base_dir = os.path.join(os.path.dirname(__file__), '..', user, 'yt', video_id)
        os.makedirs(base_dir, exist_ok=True)
        
        video_path = os.path.join(base_dir, 'video.mp4')
        audio_path = os.path.join(base_dir, 'audio.mp3')
        
        print("\n=== DOWNLOAD OPTIONS ===")
        
        # Use inquirer for choices instead of input()
        questions = [
            inquirer.List('choice',
                          message="Select download option",
                          choices=[
                              '1. Download video',
                              '2. Download audio only',
                              '3. Download both',
                              '4. Cancel'
                          ],
                          ),
        ]
        
        answers = inquirer.prompt(questions)
        choice = answers['choice'][0]  # Get first character (the number)
        
        # Try different methods in sequence
        methods = ["youtube-dl", "yt-dlp", "pytube"]
        success = False
        
        for method in methods:
            if success:
                break
                
            print(f"\nAttempting download with {method}...")
            
            if method in ["youtube-dl", "yt-dlp"]:
                tool = shutil.which(method)
                if not tool:
                    print(f"{method} not found, trying next method...")
                    continue
                    
                try:
                    if choice == '1' or choice == '3':
                        print(f"Downloading video to {video_path}...")
                        # Use -f best for good quality but faster download
                        subprocess.run([tool, '-f', 'best', '--no-playlist', 
                                      url, '-o', video_path], check=True)
                        print(f"Video downloaded successfully to {video_path}")
                        
                    if choice == '2' or choice == '3':
                        print(f"Downloading audio to {audio_path}...")
                        subprocess.run([tool, '-x', '--audio-format', 'mp3', '--no-playlist',
                                      url, '-o', os.path.join(base_dir, 'temp_audio')], check=True)
                        print(f"Audio downloaded successfully to {audio_path}")
                        
                    if choice not in ['1', '2', '3']:
                        print("Download canceled.")
                        return
                        
                    success = True
                    
                except Exception as e:
                    print(f"Error with {method}: {e}")
                    
            elif method == "pytube":
                try:
                    # Try importing pytube
                    try:
                        from pytube import YouTube
                        print("Using pytube for download...")
                    except ImportError:
                        print("pytube not installed. Installing now...")
                        subprocess.run([sys.executable, "-m", "pip", "install", "pytube"], check=True)
                        from pytube import YouTube
                    
                    # Attempt with pytube
                    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
                    
                    if choice == '1' or choice == '3':
                        print(f"Downloading video to {video_path}...")
                        stream = yt.streams.filter(progressive=True).first()
                        if not stream:
                            print("No suitable video stream found.")
                        else:
                            stream.download(output_path=os.path.dirname(video_path), filename='video.mp4')
                            print(f"Video downloaded successfully to {video_path}")
                        
                    if choice == '2' or choice == '3':
                        print(f"Downloading audio to {audio_path}...")
                        stream = yt.streams.filter(only_audio=True).first()
                        if not stream:
                            print("No suitable audio stream found.")
                        else:
                            temp_file = stream.download(output_path=os.path.dirname(audio_path), filename='temp_audio.mp4')
                            
                            # Convert to mp3 if ffmpeg is available
                            if shutil.which('ffmpeg'):
                                subprocess.run(['ffmpeg', '-i', temp_file, '-vn', audio_path], check=True)
                                os.remove(temp_file)
                            else:
                                print("ffmpeg not found. Saving audio in original format.")
                                # Just rename the file
                                os.rename(temp_file, audio_path)
                                
                            print(f"Audio downloaded successfully to {audio_path}")
                    
                    if choice not in ['1', '2', '3']:
                        print("Download canceled.")
                        return
                        
                    success = True
                    
                except Exception as e:
                    print(f"Error with pytube: {e}")
        
        if not success:
            print("\nAll download methods failed. Please try one of the following:")
            
            # Use inquirer for installation options
            install_questions = [
                inquirer.List('install',
                            message="Would you like to install one of the required tools now?",
                            choices=[
                                '1. Install yt-dlp',
                                '2. Install youtube-dl',
                                '3. Exit'
                            ],
                            ),
            ]
            
            install_answer = inquirer.prompt(install_questions)
            install_choice = install_answer['install'][0]
            
            if install_choice == '1':
                print("Installing yt-dlp...")
                subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
                print("Please retry your download.")
            elif install_choice == '2':
                print("Installing youtube-dl...")
                subprocess.run([sys.executable, "-m", "pip", "install", "youtube-dl"], check=True)
                print("Please retry your download.")
            else:
                print("Exiting without installing.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python yt-downloader.py <URL> <USER>")
        sys.exit(1)

    url = sys.argv[1]
    user = sys.argv[2]
    simple_download(url, user)
