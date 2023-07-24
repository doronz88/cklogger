import os

from setuptools import setup, find_packages

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION = '1.0.0'
PACKAGE_NAME = 'cklogger'
PACKAGES = [p for p in find_packages() if not p.startswith('tests')]


def parse_requirements():
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, 'requirements.txt')):
        with open(os.path.join(BASE_DIR, 'requirements.txt'), 'r') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs


def get_description():
    with open(os.path.join(BASE_DIR, 'README.md'), 'r') as fh:
        return fh.read()


if __name__ == '__main__':
    setup(
        version=VERSION,
        name=PACKAGE_NAME,
        description='Simple pure python utility for sniffing CloudKit usages on iDevices',
        long_description=get_description(),
        long_description_content_type='text/markdown',
        cmdclass={},
        packages=PACKAGES,
        author='DoronZ',
        install_requires=parse_requirements(),
        entry_points={
            'console_scripts': ['cklogger=cklogger.__main__:cli',
                                ],
        },
        classifiers=[
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11'
        ],
        url='https://github.com/doronz88/cklogger',
        project_urls={
            'pymobiledevice3': 'https://github.com/doronz88/cklogger'
        },
        tests_require=['pytest'],
    )
