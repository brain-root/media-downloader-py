import yt_dlp
import os
from urllib.parse import urlparse
import sys
import browser_cookie3
import json

def get_browser_cookies():
    """Get cookies from browser"""
    try:
        # Coba ambil cookies dari Chrome
        cookies = browser_cookie3.chrome()
        return cookies
    except:
        try:
            # Jika gagal, coba dari Firefox
            cookies = browser_cookie3.firefox()
            return cookies
        except:
            return None

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

def save_cookies(cookies, filename='cookies.txt'):
    """Save cookies to Netscape format file"""
    if cookies:
        with open(filename, 'w', encoding='utf-8') as f:
            for cookie in cookies:
                if cookie.domain in ['.youtube.com', '.instagram.com']:
                    f.write(f"{cookie.domain}\tTRUE\t{cookie.path}\t"
                           f"{'TRUE' if cookie.secure else 'FALSE'}\t{cookie.expires}\t"
                           f"{cookie.name}\t{cookie.value}\n")
    return filename

def download_media(url, output_path=None):
    """Download media from social media platforms"""
    try:
        platform = get_platform(url)
        print(f"Detected platform: {platform}")
        
        if output_path is None:
            output_path = os.path.join(os.getcwd(), "downloads")
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Get cookies from browser
        print("Mengambil cookies dari browser...")
        cookies = get_browser_cookies()
        cookies_file = save_cookies(cookies)
            
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'cookiefile': cookies_file,
            'ignoreerrors': True,
            'no_warnings': False,
            'quiet': False,
            'verbose': True,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 10,
            'retry_sleep_functions': {'http': lambda n: 5},
            'nocheckcertificate': True
        }
        
        # Platform specific options
        if platform == "YouTube":
            ydl_opts.update({
                'format': 'best',
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'extractor_args': {
                    'youtube': {
                        'player_client': 'all',
                        'player_skip': ['js', 'configs', 'webpage']
                    }
                }
            })
        elif platform == "Instagram":
            ydl_opts.update({
                'add_header': [
                    'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language:en-US,en;q=0.5',
                    'DNT:1'
                ],
                'extract_flat': True
            })
            
        def progress_hook(d):
            if d['status'] == 'downloading':
                sys.stdout.write('\r[download] {} of {} at {} ETA {}'.format(
                    d.get('_percent_str', '0%'),
                    d.get('_total_bytes_str', 'Unknown size'),
                    d.get('_speed_str', 'Unknown speed'),
                    d.get('_eta_str', 'Unknown ETA')
                ))
                sys.stdout.flush()
            elif d['status'] == 'finished':
                print('\nDownload completed! Converting...')
                
        ydl_opts['progress_hooks'] = [progress_hook]
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading from: {url}")
            
            try:
                # Pre-check info
                info = ydl.extract_info(url, download=False)
                if info:
                    print(f"\nTitle: {info.get('title', 'Unknown')}")
                    if info.get('duration'):
                        print(f"Duration: {info.get('duration')} seconds")
                    print(f"Type: {info.get('_type', 'Unknown')}")
                    
                    confirm = input("\nLanjutkan download? (y/n): ").lower()
                    if confirm != 'y':
                        return False
                        
                    ydl.download([url])
                    return True
                else:
                    print("Tidak dapat mengekstrak informasi media")
                    return False
                    
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e).lower()
                if "sign in to confirm" in error_msg:
                    print("\nError: YouTube meminta verifikasi. Pastikan Anda login di browser!")
                elif "video unavailable" in error_msg:
                    print("\nError: Video tidak tersedia atau private")
                else:
                    print(f"\nError downloading: {str(e)}")
                return False
            
        print(f"\nDownload completed successfully! Files saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return False

def main():
    print("=== Social Media Downloader ===")
    print("Supported platforms: YouTube, Instagram, Twitter, Facebook, TikTok")
    print("Press Ctrl+C to exit")
    print("===========================")
    
    while True:
        try:
            url = input("\nMasukkan link media sosial: ").strip()
            
            if url.lower() == 'exit':
                print("Program terminated.")
                break
                
            if not url:
                print("Link tidak boleh kosong!")
                continue
                
            custom_path = input("Masukkan folder output (kosongkan untuk default): ").strip()
            output_path = custom_path if custom_path else None
            
            success = download_media(url, output_path)
            
            if success:
                print("\nIngin download media lain? (y/n)")
                choice = input().lower()
                if choice != 'y':
                    print("Program terminated.")
                    break
            else:
                print("\nDownload gagal. Coba lagi? (y/n)")
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
