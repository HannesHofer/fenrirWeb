from setuptools import setup

setup(
    name='fenrirApp',
    version='0.1.0',
    long_description=__doc__,
    packages=['fenrirApp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Bottle', 'jinja2', 'bcrypt', 'fenrir @ https://github.com/HannesHofer/fenrir/releases/download/0.3.0/fenrir-0.3.0-py3-none-any.whl'],
    entry_points={'console_scripts': ['fenrirApp = fenrirApp.main:main', ]},
)
