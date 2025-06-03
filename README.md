Web Resource Downloader
Flask app to download website resources (HTML, CSS, JS, images, videos). Black-themed, responsive UI. Sections hidden until download succeeds. Uses Python, Flask, BeautifulSoup, jQuery.
Setup

Clone: git clone https://github.com/your-username/web-resource-downloader.git
Install: pip install flask requests beautifulsoup4 validators
Run: python test.py

Usage
Visit http://localhost:5000, enter a URL, click "Download" to view resources.
Files

test.py: Backend logic.
static/style.css: Black-themed CSS.
templates/index.html: Front-end UI.

License
MIT
Web Resource Downloader
A Flask-based web application that enables users to download and view resources (HTML, CSS, JavaScript, images, and videos) from any website by entering its URL. The application features a modern, high-contrast black-themed UI with a responsive design. Resource sections are hidden until a successful download, ensuring a clean and intuitive user experience. Built with Python, Flask, BeautifulSoup, and jQuery, with robust error handling and logging.
Features

Resource Downloading: Extracts HTML, CSS, JavaScript, images, and videos from a provided website URL.
Dynamic UI: Displays downloaded resources in dedicated sections, visible only after a successful download.
Black Theme: High-contrast, modern dark theme with animations and responsive design.
Error Handling: Validates URLs, handles network errors, and logs issues for debugging.
Media Support: Downloads images and videos, including <source> tags within <video> elements.
Responsive Design: Optimized for both desktop and mobile devices.

Prerequisites

Python 3.6+
Flask (pip install flask)
Requests (pip install requests)
BeautifulSoup4 (pip install beautifulsoup4)
Validators (pip install validators)
A modern web browser (for jQuery CDN and UI rendering)

Installation

Clone the repository:git clone https://github.com/your-username/web-resource-downloader.git
cd web-resource-downloader


Create and activate a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install flask requests beautifulsoup4 validators


Ensure the templates folder contains index.html and the static folder contains style.css.

Usage

Run the Flask application:python test.py


Open a web browser and navigate to http://localhost:5000.
Enter a valid website URL (e.g., https://example.com) in the input field and click "Download".
View the downloaded HTML, CSS, JavaScript, images, and videos in their respective sections, which appear only after a successful download.
Error messages will display if the URL is invalid or the download fails.

File Structure

test.py: Main Flask application with backend logic for downloading and serving resources.
static/style.css: CSS file defining the black-themed, responsive UI.
templates/index.html: HTML template for the front-end interface, using jQuery for dynamic updates.
downloads/: Folder where downloaded resources (HTML, CSS, JS, images, videos) are saved.

Example

Enter https://example.com in the input field.
Click "Download".
The page will display:
HTML code in a formatted <pre> block.
CSS code from linked stylesheets.
JavaScript code from external scripts.
Images and videos downloaded from the website, displayed in the media section.



Notes

Resource Limitations: Some websites may block requests due to CORS, rate-limiting, or other restrictions. The application includes error handling to manage such cases.
File Naming: Resources are saved with their original names or generated names (e.g., style_{hash}.css) if the original name is unavailable.
Dependencies: The application uses a jQuery CDN for AJAX requests. Ensure internet access for the CDN or host jQuery locally.
Logging: Errors and warnings are logged to the console for debugging.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for bug reports, feature requests, or improvements.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Flask, BeautifulSoup4, and jQuery.
Inspired by the need for a simple tool to analyze and download web resources.

