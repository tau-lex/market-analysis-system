from setuptools import setup, find_packages

import mas_tools


setup(
    name='mas_tools',
    version=mas_tools.__version__,
    packages=find_packages(),
    long_description=open('mas_tools/README.md', encoding='utf-8').read(),
    keywords=['trade', 'ml'],
    url='https://github.com/terentjew-alexey/market-analysis-system',
    author='Terentyev Aleksey',
    author_email='terentjew.alexey@ya.ru',
    license='MIT',
#    include_package_data=True,
    install_requires=[
            'numpy', 'pandas', 'matplotlib',
            'scikit-learn', 'keras>=2.1', 'tensorflow>=1.6',
            'gym', 'keras-rl'
        ]
)