import pipeline_caller
from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name = "ITU-Turkish-NLP-Pipeline-Caller",
    version = pipeline_caller.version,
    packages = find_packages(),
    scripts = ['pipeline_caller.py'],
    py_modules=['pipeline_caller'],
    author = "Ferit Tunçer",
    author_email = "ferit.tuncer@autistici.org",
    description = "A wrapper tool to use ITU Turkish NLP Pipeline API",
    license = "GPLv2",
    keywords = "ITU Turkish NLP Pipeline",
    url = "https://github.com/ferittuncer/ITU-Turkish-NLP-Pipeline-Caller",
)
