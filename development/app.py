# cloudflared tunnel --url localhost:8080 *> "C:\Users\MD SUFYAN KHAN\Desktop\projects\6th-sem-project\development\output.txt"

from datetime import datetime
from io import BytesIO
import os
from flask import Flask, redirect, render_template, request, send_file, url_for
from pytubefix import YouTube
from device_detector import DeviceDetector

app = Flask(__name__ , static_folder='static')

def deletefile(file_path):
    """Delete the specified file if it exists."""
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

def log_user_activity(userName):
    # Get the current time and format as dd-mm-yyyy HH:MM:SS
    current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    # Format the log entry
    log_entry = f"{userName} logged in at {current_time}\n\n"
    
    # Append the log entry to 'serve.txt'
    with open("logs/users.txt", "a") as file:
        file.write(log_entry)

def log_user_logout(user):
    # Get the current time in dd mm yyyy format
    current_time = datetime.now().strftime('%d %m %Y  %H:%M:%S')
    
    # Open the file in append mode and write the log entry
    with open("logs/users.txt", "a") as file:
        file.write(f"{user} logged out at {current_time}\n\n")

def write_to_file(first, second):
    # Open the file in append mode ('a')
    with open("logs/whoIswho.txt", "a") as file:
        # Write the formatted string to the file
        file.write(f"{first} is {second}\n\n")

def append_client_info(file_path , req , url):
    """Append detailed client device info to the specified file."""

    # Get User-Agent string and client IP
    user_agent_string = request.headers.get('User-Agent')  # User-Agent details
    client_ip = request.remote_addr  # Client's IP address
    
    # Parse User-Agent string using DeviceDetector
    dd = DeviceDetector(user_agent_string).parse()
    
    # Extract device details
    device_type = dd.device_type() or "Unknown Device Type"  # Device type (mobile, tablet, etc.)
    os = f"{dd.os_name() or 'Unknown OS'} {dd.os_version() or 'Unknown Version'}"  # OS name and version
    browser = f"{dd.client_name() or 'Unknown Browser'} {dd.client_version() or 'Unknown Version'}"  # Browser and version
    
    # Get current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
    
    # Prepare data to append
    info = (f"At: {date_time}, Device Type: {device_type}, "
            f"OS: {os}, Browser: {browser}, requested: {req} of YouTube({url}) \n\n")
    
    # Append information to the file
    with open(file_path, 'a') as file:
        file.write(info)

def check_youtube_url(url):
    try:
        YouTube(url)
        return True
    except Exception as e:
        print(f"Invalid URL: {e}")
        return False

def getAudio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    path = audio_stream.download(output_path='./audio')
    return path

def getMpFour(link):
    
    yt = YouTube(link)
    
    video = yt.streams.get_highest_resolution()
    filePath = video.download('./video')
    return filePath

@app.route('/whoIsWho/<first>/<second>')
def whoIsWho(first,second):
    write_to_file(first,second)
    return ''

@app.route('/userLoggedOut/<user>')
def userLoggdOut(user):
    log_user_logout(user)
    return ''

@app.route('/users/<userName>')
def start(userName):
    log_user_activity(userName)
    return ''
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/redirect/<arg>')
def redirect(arg):
    return f"{arg} not found"


@app.route('/video/<path:url>')
def video(url):
    if check_youtube_url(url):
        append_client_info('logs/serve.txt', "video", url)
        video = getMpFour(url)  # Path to the video file

        # Read the file into memory using BytesIO
        with open(video, 'rb') as f:
            file_data = BytesIO(f.read())

        response = send_file(file_data, as_attachment=True, download_name=os.path.basename(video))

        # Safely delete the file after sending it
        try:
            os.remove(video)
        except Exception as e:
            print(f"Error deleting file: {e}")

        return response
    
@app.route('/audio/<path:url>')
def audio(url):
    if check_youtube_url(url):
        append_client_info('logs/serve.txt', "Audio", url)
        audio = getAudio(url)  # Path to the audio file

        # Read the file into memory using BytesIO
        with open(audio, 'rb') as f:
            file_data = BytesIO(f.read())

        response = send_file(file_data, as_attachment=True, download_name=os.path.basename(audio))

        try:
            os.remove(audio)  # Safely delete the file
        except Exception as e:
            print(f"Error deleting file: {e}")

        return response

    return redirect(url_for('index'))

app.url_map.strict_slashes = False

# if __name__ == '__main__':
#     app.url_map.strict_slashes = False
#     app.run(debug=False) 