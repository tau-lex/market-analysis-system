from setuptools import setup

import market-analysis-system


setup(
    name='market analysis system',
    version=market-analysis-system.__version__,
    packages=['market-analysis-system'],
    long_description=open('market-analysis-system/readme.md').read(),
    keywords='trade',
    url='https://github.com/terentjew-alexey/market-analysis-system',
    author='Terentyev Aleksey',
    author_email='terentjew.alexey@ya.ru',
    license='MIT',
#    include_package_data=True,
    install_requires=[
            'keras', 'numpy', 'matplotlib', 'sklearn'
        ]
)