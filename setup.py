from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='Housou',
    version='0.1',
    description='NHK news articles morphological frequency analysis',
    long_description=readme(),
    author='Luke Beck',
    url='https://github.com/lukebeck/housou',
    py_modules=['housou'],
    install_requires=[
        'lxml',
        'mecab-python3',
        'selenium'
    ],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['housou=housou:main','housou-analyse=housou:analyse'],
    }
)
