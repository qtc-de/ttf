import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttf",
    version="1.1.0",
    author="Tobias Neitzel",
    author_email="qtc_de@outlook.com",
    description="ttf - A library to create component based console output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["termcolor", "pyparsing"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
)
