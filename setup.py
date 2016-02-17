from setuptools import setup, find_packages
setup(
    name = "ITU Turkish NLP Pipeline Caller",
    version = "1.0.0",
    packages = find_packages(),
    scripts = ['pipeline_caller.py'],
    py_modules=['pipeline_caller'],
    author = "Ferit Tunçer",
    author_email = "ferit.tuncer@autistici.org",
    description = "A wrapper tool to use ITU Turkish NLP Pipeline API",
    license = "GNUv2",
    keywords = "ITU Turkish NLP Pipeline",
    url = "https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller",
)
