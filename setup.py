
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sneratio",
    version="0.1.0",
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
    python_requires='>=3.6',

    include_package_data=True,
    package_data = {
        'sneratio': ['data/mass_numbers/*',
                    'data/solar/*',
                    'data/test_data/*',
                    'data/yields/cc/nomoto_2006/*',
                    'data/yields/cc/nomoto_2013/*',
                    'data/yields/cc/tsujimoto/*',
                    'data/yields/Ia/iwamoto/*']
    },

    install_requires=[
        "pyside2>=5.13.2",
        "pandas>=1.1.3",
        "matplotlib>=3.3.2"
    ],
)
