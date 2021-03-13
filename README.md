# htmlocto

htmlocto is a lightweight static site generator. It uses Python's built-in string.Template as the template engine and the markdown module for rendering pages to HTML.

Currently it supports rendering regular site pages (no blog list rendering).

## Requirements

* Python 3.6+
* setuptools 46.4.0+ (for installation)
* Markdown

## Installation

From source:

```
git clone https://github.com/jotorre/htmlocto.git
cd htmlocto
python setup.py install
```

If the above installation fails, update setuptools to 46.4.0 or later.

## Usage

### 1. Initiate the site's structure
```
htmlocto --init
```

htmlocto will create the following:

* pages directory (put the pages for the site here in markdown format)
* output directory (rendered html gets placed here)
* config.json

### 2. Supply the HTML template (template.html)

After rendering the markdown content, htmlocto will store the content in a dictionary with the key of **main_content**. So at minimum the template should have this placeholder ($main_content) in the body of the HTML template. 

Optionally, metadata can be added at the top of the markdown file (parsed using markdown's meta extension) and these are stored in the same dictionary with other keys and used in the overall page rendering, so add these exact placeholders accordingly (ex. **title** metadata as **$title**) in the template.

Save the template as **template.html** inside the template directory.

### 3. Write content for the pages

Write and save the markdown file with .md extension inside the pages directory.

### 4. Render the pages

Execute with no arguments:

```
htmlocto
```

Pages are rendered and placed in the output directory with the same filename as the original, replacing the extension with .html.