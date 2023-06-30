import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sleepy_module",
    version="0.1.0",
    author="Feng Liang",
    author_email="feng.liang@kaust.edu.sa",
    description="""Sleepy module in Python that "falls sleep" periodically""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ifsheldon/sleepy_module",
    project_urls={
        "Bug Tracker": "https://github.com/ifsheldon/sleepy_module/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["apscheduler"]
)
