from setuptools import setup, find_packages
from src.sps import __version__ as version

with open("README.rst", encoding="UTF-8") as f:
    readme = f.read()

setup(
    name="sps",
    version=version,
    description="CLI searching for packages in SUSE products.",
    long_description=readme,
    author="Jonas Forsberg",
    author_email="jonas.forsberg@suse.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["PTable", "requests"],
    include_package_data=True,
    package_data = {
        "sps": ["completion.sh"]
        },
    entry_points={
        "console_scripts": [
            "sps=sps.cli:main",
            ]
    }
)
