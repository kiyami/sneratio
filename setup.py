
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sneratio",
    version="0.3.0",
    author="M.Kıyami ERDİM",
    author_email="kiyami_erdim@hotmail.com",

    description="Supernova Ratio Calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/kiyami/sneratio",

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',

    include_package_data=True,
    package_data = {
        'sneratio/src': ['data/*']
    },

    install_requires=[
        "flask>=1.1.2",
        "pandas>=1.2.1",
        "matplotlib>=3.3.3",
        "scipy>=1.6.0",
    ],
)
