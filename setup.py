from setuptools import setup


setup(name='python-toggl',
      version='0.1.2',
      description='Python Wrapper for Toggl API',
      url='https://github.com/swappsco/python-toggl',
      author='mechastorm',
      author_email='dev@swapps.co',
      license='MIT',
      packages=['toggl'],
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'httpretty'],
      zip_safe=False)
