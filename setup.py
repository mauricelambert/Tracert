from setuptools import setup

setup(
    name="Tracert",
    version="0.0.1",
    py_modules=["Tracert"],
    install_requires=["scapy", "PythonToolsKit"],
    author="Maurice Lambert",
    author_email="mauricelambert434@gmail.com",
    maintainer="Maurice Lambert",
    maintainer_email="mauricelambert434@gmail.com",
    description="This package implements a traceroute tool faster than traceroute/tracert executable.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mauricelambert/Tracert",
    project_urls={
        "Documentation": "https://mauricelambert.github.io/info/python/code/Tracert.html",
        "Executable": "https://mauricelambert.github.io/info/python/code/Tracert.pyz",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: System :: Networking",
        "Natural Language :: English",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["Tracert = Tracert:main"],
    },
    keywords=[
        "network",
        "traceroute",
        "tracert",
        "trace",
        "ping",
        "debug",
    ],
    platforms=["Windows", "Linux", "MacOS"],
    license="GPL-3.0 License",
)
