import io
import os
from setuptools import setup




__version__ = '0.3a'
__author__ = 'Fernando de Assis Rodrigues'

description = 'Attini Client/Server'
here = os.path.abspath(os.path.dirname(__file__))

# load requirements
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

# load README
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as doc_file:
    documentation = '\n' + doc_file.read()



setup(
    name='attini',
    version=__version__,
    description=description,
    long_description=documentation,
    author=__author__,
    author_email='fernando@rodrigues.pro.br',
    maintainer="Fernando de Assis Rodrigues",
    url='https://rodrigues.pro.br',
    download_url="https://dadosabertos.info/projects/attini/master.zip",
    packages=['attini'],
    py_modules='attini',
    license="GPLv3",
    keywords=["attini", "automation", "bot"],
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Environment :: ARM",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License v3",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: Unix",
                 "Programming Language :: Python",
                 "Programming Language :: SQL",
                 "Topic :: Internet :: Browsers",
                 "Topic :: Other/Nonlisted Topic :: Automation :: Selenium",
                 "Topic :: Utilities",
                 "Natural Language :: English"],
    install_requires=dependencies,
    include_package_data=True,
    python_requires=">=2.7",
    platforms=["arm", "linux", "linux2", "darwin"]
)



