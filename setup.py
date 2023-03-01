from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='noisymax',
    version='0.1',
    description='...',
    long_description=long_description,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Differential Privacy :: Statistics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='Differential Privacy, Report Noisy Max',
    packages=find_packages(exclude=['tests']),
    install_requires=['numpy', 'tqdm', 'numba'],
    extras_require={
        'test': ['pytest-cov', 'pytest', 'coverage', 'flaky', 'scipy'],
    },
)