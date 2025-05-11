from setuptools import setup, find_packages

setup(
    name='notification_service',
    version='0.1.0',
    description='Email sender with CSS inlining using premailer',
    author='Rohan Raut',
    author_email='rohanraut124@gmail.com',
    include_package_data=True,
    package_data={
        'notification_service': ['assets/logo.png'],
    },
    packages=find_packages(),
    install_requires=[
        'premailer'
    ],
    python_requires='>=3.6',
    license_files=['LICENSE.md']
)
