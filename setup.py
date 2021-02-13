
import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name='toolcache',
    version='0.0.1',
    description='makes it easy to create and configure caches in python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sslivkoff/toolcache',
    packages=setuptools.find_packages(),
    requires=[
        'orjson',
        'tooltime',
    ],
    python_requires='>=3.6',
)

