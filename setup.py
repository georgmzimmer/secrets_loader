from setuptools import setup, find_packages

setup(
    name="secrets_loader",
    version="0.1.4",
    author="Worthwhile",
    author_email="devs@worthwhile.com",
    packages=find_packages(),
    include_package_data=True,  # declarations in MANIFEST.in
    license="LICENSE",
    description="Chain Loader for AWS secrets manager secrets.",
    long_description=open("README.md").read(),
    python_requires='>=3.6',
    install_requires=['boto3', 'botocore'],
    entry_points={'console_scripts': ['secrets_loader = secrets_loader.secrets_loader:main', ]},
)
