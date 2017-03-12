from distutils.core import setup

setup(
    name='rocketchat_API',
    version='0.1',
    packages=['rocketchat_API', 'rocketchat_API.APIExceptions'],
    url='',
    license='MIT',
    author='Jorge Alberto Díaz Orozco',
    author_email='diazorozcoj@gmail.com',
    description='Python rocketchat_API wrapper for Rocket.Chat',
    install_requires=[
        'requests>=2.0.0,<3.0'
    ]
)
