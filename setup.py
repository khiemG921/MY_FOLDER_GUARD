from setuptools import setup, find_packages

setup(
    name="My Folder Guard",
    version="1.0.0",
    description="A folder protection and facial recognition-based app for securing sensitive files and folders.",
    author="Trần Gia Khiêm",
    author_email="giakhiem417@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "deepface==0.0.75",
        "opencv-python==4.8.0.74",
        "Pillow==9.1.0",
        "tk==0.1.0",
        "cryptography==41.0.0"
    ],
    entry_points={
        'console_scripts': [
            'my-folder-guard=main:main',  # Main entry point for the program
        ],
    },
)