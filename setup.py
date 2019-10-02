import setuptools

with open('README.md', 'rt') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]
setuptools.setup(
    name='mpa-gen',
    version='0.2',
    author='Baryshnikov Aleksandr (reddec)',
    author_email='owner@reddec.net',
    description='Simple generator for Go multi-page site',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/reddec/mpa-gen',
    packages=setuptools.find_packages(),
    install_requires=install_reqs,
    package_data={
        '': ['*.jinja2'],
    },
    setup_requires=['wheel'],
    entry_points={
        "console_scripts": ['mpa-gen = mpagen.__main__:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Utilities'
    ]
)
