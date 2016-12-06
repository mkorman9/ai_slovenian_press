from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

version = '0.1'

setup(
    name='ai_slovenian_press',
    author='Michal Korman',
    author_email='m.korman94@gmail.com',
    packages=find_packages(exclude=('tests',)),
    version=version,
    classifiers=[],
    install_requires=[requirement for requirement in requirements if len(requirement) > 0]
)
