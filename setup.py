from setuptools import setup, find_packages

def read_version():
    with open('RELEASE.txt') as f:
        return f.readline().strip()

setup(
    name='tombolamanager',
    version=read_version(),
    author='Francesco Dallanoce',
    author_email='dallanoce.fd@gmail.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dallanoce/tombola-manager',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'pyinstaller',
    ],
)