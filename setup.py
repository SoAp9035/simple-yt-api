from setuptools import setup, find_packages


setup(
    name="simple-yt-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "youtube-transcript-api"
    ],
    author="Ahmet Burhan Kayalı",
    author_email="ahmetburhan1703@gmail.com",
    description="A simple and easy-to-use YouTube API Wrapper",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/SoAp9035/simple-yt-api",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Video",
        "Topic :: Text Processing :: Markup :: HTML",

        "License :: OSI Approved :: MIT License",
    ],
    keywords=["simple", "youtube", "api", "wrapper"]
)