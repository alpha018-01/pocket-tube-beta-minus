import qrcode
import re

# File containing the URLs
file_path = "logs/out.txt"

# Function to extract URLs from file content
def extract_urls(content):
    # Regular expression to find URLs
    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, content)
    return urls

try:
    # Open the file safely in read-only mode
    with open(file_path, "r") as file:
        content = file.read()  # Read the whole file content
        print("File read successfully!")  # Debugging information
except IOError as e:
    print(f"Error accessing the file: {e}")
    exit()

# Extract URLs from the file content
urls = extract_urls(content)
print(f"Extracted URLs: {urls}")  # Debugging: List all URLs

# Check if the 3rd URL exists
if len(urls) >= 3:
    third_url = urls[2]  # Get the 3rd URL
    print(f"Third URL: {third_url}")

    # Generate QR Code for the 3rd URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(third_url)
    qr.make(fit=True)

    # Save the QR Code as an image
    qr_image_path = "QRCodes/HereIsMySite.png"
    qr_img = qr.make_image(fill_color="black", back_color="white")
    try:
        qr_img.save(qr_image_path)
        print(f"QR Code for the 3rd URL saved as: {qr_image_path}")
    except IOError as e:
        print(f"Error saving QR Code: {e}")
else:
    print("Less than 3 URLs found in the file.")


# start-job -scriptblock{cloudflared tunnel --url localhost:5000 *> "out.txt"}
# start-sleep -seconds 20
# start-job -scriptblock{python app.py}
# start-sleep -seconds 10
# start-job -scriptblock{python geturl.py}
