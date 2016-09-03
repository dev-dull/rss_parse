from setuptools import setup

setup(name='rss_parse',
      version='0.1.0b1',
      description='RSS feed parser: Takes a URL and configuration dict and '
                  'returns an iterable object containing feed `<items>`',
      long_description=open('README.md', 'r').read(),
      author='Alastair Drong',
      author_email='adrong@gmail.com',
      url='https://github.com/dev-dull/rss_parse',
      license='MIT',
      py_modules=['rss_parse'],
      install_requires=['arrow', 'lxml'],
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: RSS and Atom feed parsing.',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.4',
        ],
      keywords='RSS parser xml news Atom',
      )
