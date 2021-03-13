# MIT License

# Copyright (c) 2020-2021 Joel Torres

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Lightweight static site generator."""

import os
import sys
import json
import time
from argparse import ArgumentParser
from string import Template
from markdown import Markdown

__version__ = "0.3.0"


def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as r_file_handle:
            return r_file_handle.read()
    except FileNotFoundError:
        sys.exit("octo: error[read_file]: file not found: {fpath}".format(
            fpath=file_path))
    except (PermissionError, UnicodeDecodeError):
        sys.exit("octo: error[read_file]: "
                 "unable to open or read: {fpath}".format(
                   fpath=file_path))


def write_file(file_path: str, text: str) -> None:
    with open(file_path, "w", encoding="utf-8") as w_file_handle:
        w_file_handle.write(text)


def save_config(config_file: str, config_data: dict) -> None:
    write_file(config_file, json.dumps(config_data, indent=4))


def load_config(config_file: str) -> dict:
    try:
        return json.loads(read_file(config_file))
    except json.JSONDecodeError:
        sys.exit("octo: error[load_config]: "
                 "unable to decode config, check for valid JSON")


def load_template(file_path: str) -> Template:
    return Template(read_file(file_path))


def render_html(template: Template, mappings: dict) -> str:
    try:
        return template.substitute(mappings)

    except KeyError as e:
        sys.exit("octo: error[render_html]: "
                 "metadata not used in md file, "
                 "but supplied in the template: {msg}".format(
                   msg=e))

    except ValueError as e:
        sys.exit("octo: error[render_html]: {msg} from the template".format(
            msg=e))


def render_markdown(page_text: str, md_parser: Markdown) -> dict:
    html_data = {}
    html_content = md_parser.convert(page_text)
    html_meta = md_parser.Meta

    html_data["main_content"] = html_content

    for meta_tag in html_meta:
        html_data[meta_tag] = html_meta[meta_tag][0]

    md_parser.reset()

    return html_data


def render_page(md_page_text: str, md_parser: Markdown,
                template: Template, config: dict = {}) -> str:

    page_data = render_markdown(md_page_text, md_parser)
    page_data.update(config)

    return render_html(template, page_data)


def mkdirs(pages_dir: str, output_dir: str) -> None:
    if not os.path.exists(pages_dir):
        os.mkdir(pages_dir)
        print("created {} directory "
              "(put your md pages here)".format(pages_dir))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("created {} directory "
              "(rendered html is placed here)".format(output_dir))


def init_setup(config_file: str) -> None:
    config = {}
    try:
        site_title = input("site title: ")
        site_url = input("site url: ")
        config["site_title"] = site_title
        config["site_url"] = site_url

        if os.path.isfile("template.html"):
            config["template"] = "template.html"
        else:
            while True:
                template_location = input("template location: ")
                if os.path.isfile(template_location):
                    config["template"] = template_location
                    break
                else:
                    print("template not found!")

    except KeyboardInterrupt:
        sys.exit(1)

    save_config(config_file, config)


def main():

    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="version",
                        version=__version__)
    parser.add_argument("-i", "--init", action="store_true",
                        help="initiate or re-config site's structure and exit")
    parser.add_argument("-r", "--root", action="store_true",
                        help="save rendered pages at the top "
                             "of the execution directory")
    args = parser.parse_args()

    pages_dir = "pages"
    output_dir = "output"
    config_file = "config.json"

    if args.init:
        mkdirs(pages_dir, output_dir)
        init_setup(config_file)

        sys.exit()

    if not os.path.exists(config_file) or \
       not os.path.exists(pages_dir) or \
       not os.path.exists(output_dir):
        sys.exit("octo: error[main]: site has not been initialized, "
                 "please run with --init first")

    config = load_config(config_file)

    html_template = load_template(config["template"])

    md_parser = Markdown(extensions=["meta"])

    if args.root:
        output_dir = ""

    total_pages = 0
    start_render_time = time.time()

    for md_page in os.listdir(pages_dir):
        if not md_page.endswith(".md"):
            continue

        page_path = os.path.join(pages_dir, md_page)

        if not os.path.isfile(page_path):
            continue

        md_page_text = read_file(page_path)

        print("octo: rendering page {}".format(md_page))
        html = render_page(md_page_text, md_parser, html_template, config)

        html_file_name = md_page.replace(".md", ".html")
        output_path = os.path.join(output_dir, html_file_name)

        print("octo: {ifname} -> {out}".format(
              ifname=md_page, out=output_path, ofname=html_file_name))
        write_file(output_path, html)

        total_pages += 1

    end_render_time = time.time()

    print("octo: finished rendering {} page{} in {} secs".format(
           total_pages, "" if total_pages == 1 else "s",
           round(end_render_time-start_render_time, 4)))


if __name__ == "__main__":
    main()
