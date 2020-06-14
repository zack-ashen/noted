from noted import __version__

from setuptools import setup, find_packages

install_requirements = [
    'pyfiglet>=0.8.post1',
    'PyInquirer>=1.0.3'
]

setup(
    name='noted-notes',
    version=__version__,
    author='Zachary Ashen',
    author_email='zachary.h.a@gmail.com',
    license='MIT',
    description='Noted is a cli note taking and todo app similar to google keep or any other note taking service. It '
                'is a fork of my previous project keep-cli. Notes appear as cards. You can make lists and write '
                'random ideas. ',
    url='https://github.com/zack-ashen/noted',
    long_description=open('README-pip.md').read(),
    long_description_content_type='text/markdown',
    install_requires=install_requirements,
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='cli notes todo notetaking noted',
    packages=find_packages(),
    package_data={
        "noted": ["noted/note_data/notes.json"]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'noted=noted.noted:main'
        ]
    }
)