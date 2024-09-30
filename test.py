import os
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

# Folder where downloaded resources will be saved
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Route for serving downloaded images and videos
@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    if url:
        resource_contents = download_resources(url, DOWNLOAD_FOLDER)
        return jsonify({
            "message": "Resources downloaded successfully!",
            "contents": resource_contents
        })
    else:
        return jsonify({"error": "No URL provided."})

# Function to download resources and return contents for HTML, CSS, JS, Images, and Videos
def download_resources(url, folder_path):
    response = requests.get(url)
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
        css_name = os.path.basename(urlparse(css_url).path)
        css_content += download_file(css_url, os.path.join(folder_path, css_name))
    resource_contents['CSS'] = css_content

    # Download and return JS files
    js_content = ''
    for script_tag in soup.find_all('script', src=True):
        js_url = urljoin(url, script_tag.get('src'))
        js_name = os.path.basename(urlparse(js_url).path)
        js_content += download_file(js_url, os.path.join(folder_path, js_name))
    resource_contents['JavaScript'] = js_content

    # Download and return Images
    images_content = []
    for img_tag in soup.find_all('img'):
        img_url = urljoin(url, img_tag.get('src'))
        img_name = os.path.basename(urlparse(img_url).path)
        download_file(img_url, os.path.join(folder_path, img_name))
        images_content.append(f'/downloads/{img_name}')
    resource_contents['Images'] = images_content

    # Download and return Videos
    videos_content = []
    for video_tag in soup.find_all('video'):
        video_url = urljoin(url, video_tag.get('src'))
        video_name = os.path.basename(urlparse(video_url).path)
        download_file(video_url, os.path.join(folder_path, video_name))
        videos_content.append(f'/downloads/{video_name}')
    resource_contents['Videos'] = videos_content

    return resource_contents

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return response.text if 'text' in response.headers['Content-Type'] else ''

if __name__ == '__main__':
    app.run(debug=True)
