from setuptools import setup, find_packages

import market_analysis_system


setup(
    name='market analysis system',
    version=market_analysis_system.__version__,
    packages=find_packages(),
    long_description=open('README.md', encoding='utf-8').read(),
    keywords='trade',
    url='https://github.com/terentjew-alexey/market-analysis-system',
    author='Terentyev Aleksey',
    author_email='terentjew.alexey@ya.ru',
    license='MIT',
#    include_package_data=True,
    install_requires=[
            'numpy', 'pandas', 'matplotlib',
            'scikit-learn', 'keras', 'tensorflow'
        ]
)