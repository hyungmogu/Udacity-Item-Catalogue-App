from setuptools import setup

setup(
    name = "item_catlogue",
    version = "0.4.0",
    author = "Hyungmo Gu",
    packages = ["item_catalogue"],
    inlude_package_data = True,
    install_requires = [
        "Flask==0.11.1",
        "SQLAlchemy==1.1.4",
        "Jinja2==2.8",
        "httplib2==0.9.2",
        "oauth2client==4.0.0",
        "requests==2.2.1"
        ]
    )
