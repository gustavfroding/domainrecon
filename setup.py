from setuptools import setup, find_packages

setup(
    name="domainrecon",
    version="0.2.0",
    description="CLI-verktyg för att kartlägga teknikstack för domäner",
    author="Ditt Namn",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "rich",
        "python-whois",
        "dnspython",
        "ipwhois",
        "aiohttp",
        "bs4",
    ],
    entry_points={
        "console_scripts": [
            "domainrecon = domainrecon.cli:main",
        ],
    },
)