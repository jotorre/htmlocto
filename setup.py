import setuptools

with open("README.md", "r", encoding="utf8") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name="htmlocto",
    description="Lightweight static site generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jotorre/htmlocto",
    author="Joel Torres",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Console",
        "Operating System :: OS Independent"
    ],
    py_modules=["htmlocto"],
    install_requires=[
        "markdown==3.3.3"
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "htmlocto=htmlocto:main"
        ]
    }

)
