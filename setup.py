from setuptools import find_packages, setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name='geo_distributed_lru_cache',
    packages=find_packages(include=['cache', 'exceptions', 'messaging', 'utils']),
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    version='0.0.1',
    description='A geo distributed LRU cache using RabbitMQ Server.',
    license='MIT',
    classifiers=classifiers,
    keywords='lru cache redis',
    author='Lenny Siemeni',
    test_suite='tests',
    install_requires=['']
)
