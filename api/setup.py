import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="startup-generator-api",
    version="0.0.1",
    author="Mark Miller",
    author_email="mark@markmiller.space",
    description="A simple api to generate startup company names.",
    include_package_data=True,
    install_requires=[
        "boto3",
        "dnspython",
        "flask",
        "flask-caching",
        "flask-cors",
        "flask-login",
        "Flask-PyMongo",
        "jsonschema",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["startup-generator-api=StartupGeneratorAPI.cli:main"],
    },
)
