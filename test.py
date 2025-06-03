import os
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import validators
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Folder where downloaded resources will be saved
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Route for serving downloaded images and videos
@app.route('/downloads/<path:filename>')
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        return jsonify({"error": f"File not found: {filename}"}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided."}), 400
    
    # Validate URL
    if not validators.url(url):
        logger.error(f"Invalid URL provided: {url}")
        return jsonify({"error": "Invalid URL provided."}), 400
    
    try:
        resource_contents = download_resources(url, DOWNLOAD_FOLDER)
        return jsonify({
            "message": "Resources downloaded successfully!",
            "contents": resource_contents
        })
    except Exception as e:
        logger.error(f"Error downloading resources from {url}: {str(e)}")
        return jsonify({"error": f"Failed to download resources: {str(e)}"}), 500

# Function to download resources and return contents for HTML, CSS, JS, Images, and Videos
def download_resources(url, folder_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        resource_contents = {}

        # Save and return the HTML content
        html_file_path = os.path.join(folder_path, 'index.html')
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        resource_contents['HTML'] = response.text

        # Download and return CSS files
        css_content = ''
        for link_tag in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, link_tag.get('href'))
            if css_url and validators.url(css_url):
                css_name = os.path.basename(urlparse(css_url).path) or f"style_{hash(css_url)}.css"
                try:
                    css_content += download_file_content(css_url, os.path.join(folder_path, css_name))
                except Exception as e:
                    logger.warning(f"Failed to download CSS {css_url}: {str(e)}")
        resource_contents['CSS'] = css_content

        # Download and return JS files
        js_content = ''
        for script_tag in soup.find_all('script', src=True):
            js_url = urljoin(url, script_tag.get('src'))
            if js_url and validators.url(js_url):
                js_name = os.path.basename(urlparse(js_url).path) or f"script_{hash(js_url)}.js"
                try:
                    js_content += download_file_content(js_url, os.path.join(folder_path, js_name))
                except Exception as e:
                    logger.warning(f"Failed to download JS {js_url}: {str(e)}")
        resource_contents['JavaScript'] = js_content

        # Download and return Images
        images_content = []
        for img_tag in soup.find_all('img'):
            img_url = urljoin(url, img_tag.get('src'))
            if img_url and validators.url(img_url):
                img_name = os.path.basename(urlparse(img_url).path) or f"image_{hash(img_url)}.jpg"
                try:
                    download_file_content(img_url, os.path.join(folder_path, img_name))
                    images_content.append(f'/downloads/{img_name}')
                except Exception as e:
                    logger.warning(f"Failed to download image {img_url}: {str(e)}")
        resource_contents['Images'] = images_content

        # Download and return Videos (including <source> tags)
        videos_content = []
        for video_tag in soup.find_all('video'):
            # Check for direct src attribute
            video_url = urljoin(url, video_tag.get('src'))
            if video_url and validators.url(video_url):
                video_name = os.path.basename(urlparse(video_url).path) or f"video_{hash(video_url)}.mp4"
                try:
                    download_file_content(video_url, os.path.join(folder_path, video_name))
                    videos_content.append(f'/downloads/{video_name}')
                except Exception as e:
                    logger.warning(f"Failed to download video {video_url}: {str(e)}")
            # Check for <source> tags within <video>
            for source_tag in video_tag.find_all('source'):
                src_url = urljoin(url, source_tag.get('src'))
                if src_url and validators.url(src_url):
                    video_name = os.path.basename(urlparse(src_url).path) or f"video_{hash(src_url)}.mp4"
                    try:
                        download_file_content(src_url, os.path.join(folder_path, video_name))
                        videos_content.append(f'/downloads/{video_name}')
                    except Exception as e:
                        logger.warning(f"Failed to download video source {src_url}: {str(e)}")
        resource_contents['Videos'] = videos_content

        return resource_contents
    except Exception as e:
        logger.error(f"Error in download_resources: {str(e)}")
        raise

def download_file_content(url, file_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        if 'text' in response.headers.get('Content-Type', '').lower():
            return response.text
        return ''
    except Exception as e:
        logger.error(f"Error downloading {url}: {str(e)}")
        return ''

if __name__ == '__main__':
    app.run(debug=True)