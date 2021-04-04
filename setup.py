from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-site-settings",
    version="0.1",
    scripts=[],
    author="Mikhail Badrazhan",
    author_email="contact@devilweb.ru",
    description="Site settings management",
    long_description=long_description,
    install_requires=[
        'django'
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/migelbd/django-site-settings",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)