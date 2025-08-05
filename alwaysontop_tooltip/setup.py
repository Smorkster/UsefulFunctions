from setuptools import setup, find_packages

setup(
    name = "alwaysontop_tooltip",
    version = "0.1.0",
    description = "A Tkinter tooltip widget that always stays on top.",
    author = "Smorkster",
    author_email = "smorkster@gmail.com",
    packages = find_packages(),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.12.3",
)
