import unittest
import os
from htmlocto import *
from string import Template
from markdown import Markdown

md_parser = Markdown(extensions=["meta"])


class Test(unittest.TestCase):
    def test_render_html(self):
        output = render_html(Template("<body>${main_content}</body>"),
                             {"main_content": "<p>render sample</p>"})

        self.assertEqual(output, "<body><p>render sample</p></body>")

    def test_render_html_extra(self):
        output = render_html(Template(
                             "<body>${main_content}"
                             "<footer>${author}</footer></body>"),
                             {"main_content": "<p>another sample</p>",
                              "author": "Joel Torres"})

        self.assertEqual(output, "<body><p>another sample</p>"
                                 "<footer>Joel Torres</footer></body>")

    def test_render_markdown(self):
        output = render_markdown("sample markdown", md_parser)

        self.assertEqual(output, {"main_content": "<p>sample markdown</p>"})

    def test_render_markdown_with_meta(self):
        output = render_markdown("title: test\n\nsample markdown",
                                 md_parser)

        self.assertEqual(output, {"title": "test",
                                  "main_content": "<p>sample markdown</p>"})

    def test_render_markdown_with_meta_2(self):
        output = render_markdown("title: test\ntag: py\n\nsample markdown",
                                 md_parser)

        self.assertEqual(output, {"title": "test", "tag": "py",
                                  "main_content": "<p>sample markdown</p>"})

    def test_render_page(self):
        output = render_page("sample markdown", md_parser,
                             Template("<body>${main_content}</body>"))

        self.assertEqual(output, "<body><p>sample markdown</p></body>")

    def test_render_page_with_multiple(self):
        output = render_page("title: test\n\nsample markdown",
                             md_parser,
                             Template("<head><title>${title}</title>"
                                      "</head><body>${main_content}</body>"))

        self.assertEqual(output, "<head><title>test</title>"
                                 "</head><body><p>sample markdown</p></body>")

    def test_render_page_with_config(self):
        config = {"site_title": "htmlocto",
                  "author": "Joel Torres"}
        output = render_page("title: test with config\n\nanother sample",
                             md_parser,
                             Template("<head><title>${site_title} - ${author}"
                                      "</title></head><body><h1>${title}</h1>"
                                      "\n${main_content}</body>"),
                             config)

        self.assertEqual(output, "<head><title>htmlocto - Joel Torres</title>"
                                 "</head><body><h1>test with config</h1>\n"
                                 "<p>another sample</p></body>")

    def test_read_file(self):
        data = read_file("setup.cfg")
        self.assertIn("[metadata]", data)

    def test_write_file(self):
        write_file("test_write.txt", "htmlocto")
        file_exists = os.path.exists("test_write.txt")
        self.assertEqual(file_exists, True)

    def test_config_op(self):
        save_config("test_config.json", {"template": "test.html"})
        config = load_config("test_config.json")
        self.assertEqual(config["template"], "test.html")


if __name__ == "__main__":
    unittest.main()
