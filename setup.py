from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easypy-lang",
    version="2.1.1",
    author="Vadik Goel",
    author_email="vadikgoel1@gmail.com",
    description="A simple, powerful language for AI, ML, and apps - No coding experience needed!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/VadikGoel/easypy-lang",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.9",
    install_requires=[
        "rich>=13.7.0",
        "requests>=2.28.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "discord.py>=2.0.0",
        "openai>=1.0.0",
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "easypy=easypy_lang.cli:main",
            "easy=easypy_lang.cli:main",
        ],
    },
    include_package_data=True,
)
