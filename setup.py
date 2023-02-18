from setuptools import setup

setup(
    name='fenrirApp',
    version='0.1.0',
    long_description=__doc__,
    packages=['fenrirApp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Bottle', 'fenrir', 'jinja2', 'bcrypt'],
    entry_points={'console_scripts': ['fenrirApp = fenrirApp.main:main', ]},
)
