from setuptools import setup, find_packages

setup(
    name="zorkian-aoc",
    version="0.1",
    description="zorkian's solutions for https://adventofcode.com/",
    url="https://github.com/zorkian/advent-of-code",
    author="zorkian",
    author_email="mark@qq.is",
    long_description="Nothing.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
        "advent-of-code-data >= 2.0.0",
        "click >= 8.1.7",
    ],
    packages=find_packages(),
    entry_points={
        "adventofcode.user": ["zorkian = aoc:solver"],
    },
)
