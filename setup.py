from setuptools import setup

setup(
    name='fenrirWeb',
    version='0.1.0',
    long_description=__doc__,
    authors=['Hannes Hofer <Hannes.Hofer@gmail.com>'],
    description='use FenrirWeb as WebInterface for fenrir in order to show and configure VPN route enforcement',
    packages=['fenrirWeb'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Bottle', 'jinja2', 'bcrypt', 'fenrir @ https://github.com/HannesHofer/fenrir/releases/download/0.3.0/fenrir-0.3.0-py3-none-any.whl'],
    entry_points={'console_scripts': ['fenrirWeb = fenrirWeb.main:main', ]},
)
