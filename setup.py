
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snratio",
    version="0.0.1",
    author="M.Kıyami ERDİM",
    author_email="kiyami@mail.com",
    description="supernova ratio calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kiyami/kython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data = {
        'snratio': ['data/mass_numbers/*'],
        'snratio': ['data/solar/*'],
        'snratio': ['data/test_data/*'],
        'snratio': ['data/yields/cc/nomoto_2006/*'],
        'snratio': ['data/yields/cc/nomoto_2013/*'],
        'snratio': ['data/yields/cc/tsujimoto/*'],
        'snratio': ['data/yields/Ia/iwamoto/*']
    }
)