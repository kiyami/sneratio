
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sneratio",
    version="1.0.0",
    author="M.Kıyami ERDİM",
    author_email="kiyamierdim@gmail.com",

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
        'sneratio/src': ['data/*'],
        'sneratio/src': ['info.json']
    },

    install_requires=[
        "flask",
        "pandas",
        "matplotlib",
        "scipy",
        "gunicorn",
        "python-dotenv",
        "redis",
        "rq",
    ],
)
