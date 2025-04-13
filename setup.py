from setuptools import setup, find_packages


setup(
    name="simple-yt-api",
    version="1.1.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "beautifulsoup4>=4.13.3",
        "youtube-transcript-api>=0.6.3"
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