from setuptools import setup, find_packages

DESCRIPTION = "Yandex mail for domain user management Django app"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: System Administrators',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django',
    'Topic :: Communications :: Email :: Post-Office',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: BSD License',
    ]

setup(name='yandexmail',
    packages=find_packages(exclude=('tests', 'tests.*')),
    author='Vasily Alexeev',
    author_email='mail@v-alexeev.ru',
    url='http://v-alexeev.ru/',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'nginxmailauth',
    ],
    dependency_links = [
        'http://github.com/V-Alexeev/nginxmailauth/tarball/master#egg=nginxmailauth-dev',
    ],
    version='0.5',
)