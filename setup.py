try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Topic :: Documentation',
    'Topic :: Utilities',
]

setup(
    name='woman',
    use_scm_version=True,
    description='command line interface for explainshell.com',
    url='http://github.com/Arnie97/woman',
    author='Arnie97',
    author_email='arnie97@gmail.com',
    license='MIT',
    py_modules=['woman'],
    setup_requires=['setuptools_scm'],
    install_requires=['pyquery >= 1.2.3'],
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'woman=woman:main',
        ],
    },
    zip_safe=True,
)
