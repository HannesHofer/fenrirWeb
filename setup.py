from setuptools import setup
import fenrirWeb

setup(
    name='fenrirWeb',
    version=fenrirWeb.__version__,
    long_description="""Fenrir provides a user friendly way to route all traffic from configured trough a VPN tunnel.

FenrirWeb is a webinterface for viewing/ configuring fenrir.
    """,
    authors=['Hannes Hofer <Hannes.Hofer@gmail.com>'],
    description='use FenrirWeb as WebInterface for fenrir in order to show and configure VPN route enforcement',
    packages=['fenrirWeb'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Bottle', 'jinja2', 'bcrypt', 'fenrircore'],
    entry_points={'console_scripts': ['fenrirWeb = fenrirWeb.main:main', ]},
)
