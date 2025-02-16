import yt_dlp
import os
from urllib.parse import urlparse

def get_platform(url):
    """Determine social media platform from URL"""
    domain = urlparse(url).netloc.lower()
    
    platforms = {
        'youtube.com': 'YouTube',
        'youtu.be': 'YouTube', 
        'instagram.com': 'Instagram',
        'twitter.com': 'Twitter',
        'x.com': 'Twitter',
        'facebook.com': 'Facebook',
        'fb.com': 'Facebook',
        'tiktok.com': 'TikTok'
    }
    
    for key, value in platforms.items():
        if key in domain:
            return value
    return "Unknown"

def download_media(url, output_path=None):
    """Download media from social media platforms"""
    try:
        # Configure yt-dlp options
        platform = get_platform(url)
        print(f"Detected platform: {platform}")
        
        if output_path is None:
            output_path = os.path.join(os.getcwd(), "downloads")
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'no_warnings': False,
            'quiet': False,
            'extract_flat': False,
            'cookiefile': 'cookies.txt',  # Optional: for private content
        }
        
        # Add platform-specific options
        if platform == "Instagram":
            ydl_opts['add_header'] = ['User-Agent:Mozilla/5.0']
        elif platform == "TikTok":
            ydl_opts['format'] = 'best[ext=mp4]'
            
        # Initialize downloader
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading from: {url}")
            ydl.download([url])
            
        print(f"Download completed successfully! Files saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def main():
    print("=== Social Media Downloader ===")
    print("Supported platforms: YouTube, Instagram, Twitter, Facebook, TikTok")
    print("Press Ctrl+C to exit")
    print("===========================")
    
    while True:
        try:
            # Get URL input from user
            url = input("\nMasukkan link media sosial: ").strip()
            
            if url.lower() == 'exit':
                print("Program terminated.")
                break
                
            if not url:
                print("Link tidak boleh kosong!")
                continue
                
            # Ask for custom output path (optional)
            custom_path = input("Masukkan folder output (kosongkan untuk default): ").strip()
            output_path = custom_path if custom_path else None
            
            # Download the media
            success = download_media(url, output_path)
            
            if success:
                print("\nIngin download media lain? (y/n)")
                choice = input().lower()
                if choice != 'y':
                    print("Program terminated.")
                    break
                    
        except KeyboardInterrupt:
            print("\nProgram terminated.")
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {str(e)}")
            continue

if __name__ == "__main__":
    main()
