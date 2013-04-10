#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import fnmatch
import glob

from setuptools import setup, find_packages

from opps import timelinejs


install_requires = ["opps", "jsonfield"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']


try:
    long_description = open('README.md').read()
except:
    long_description = timelinejs.__description__


## ????
def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


def find_data_files(srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    def walk_helper(arg, dirname, files):
        if '.svn' in dirname:
            return
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)

                if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                    names.append(filename)
        if names:
            lst.append((dirname, names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list

files = find_data_files('opps/timelinejs/', '*.*')

## ????

setup(
    name='opps-timelinejs',
    namespace_packages=['opps', 'opps.timelinejs'],
    version=timelinejs.__version__,
    description=timelinejs.__description__,
    long_description=long_description,
    classifiers=classifiers,
    keywords='Timeline JS for  opps cms django apps magazines websites',
    author=timelinejs.__author__,
    author_email=timelinejs.__email__,
    url='http://oppsproject.org',
    download_url="https://github.com/YACOWS/opps-timelinejs/tarball/master",
    license=timelinejs.__license__,
    packages=find_packages(exclude=('doc', 'docs',)),
    data_files=files,
    package_dir={'opps': 'opps'},
    install_requires=install_requires,
    include_package_data=True,
    package_data={
        'timelinejs': ['templates/*', 'templatetags/*', 'static/*']
    }
)
