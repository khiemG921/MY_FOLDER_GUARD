from setuptools import setup, find_packages

setup(
    name="My_Folder_Guard",
    version="1.0.0",
    packages=find_packages(include=["core", "core.*"]),  # Include core and its sub-packages
    include_package_data=True,
    install_requires=[
        "deepface>=0.0.75",    # Specify required packages
        "tkinter",             # You may need to remove this if it causes issues since tkinter is part of Python
        "opencv-python>=4.5",  # For cv2
        "Pillow>=8.2.0",       # For image processing
        "pycryptodome>=3.9.9"  # PyCryptodome for encryption (provides Crypto library)
    ],
    entry_points={
        "console_scripts": [
            "my_project=core.main:main",  # Entry point for the main function
        ]
    },
    package_data={
        # Include all files in these folders (like facial images, keys, settings, etc.)
        '': ['data/facial_images/*', 'data/folder_table/*', 'data/images/*', 'data/key/*', 'data/settings/*'],
    },
    author="Trần Gia Khiêm",
    author_email="giakhiem417@gmail.com",
    description="A project for folder proctection",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/khiemG921/My_Folder_Guard.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python versions
)
