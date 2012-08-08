from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name = 'buildbot_patterns',
    version = version,
    description = "Simple reusable patterns to help simplify buildbot configuration",
    keywords = "buildbot ci",
    url = "http://github.com/Jc2k/buildbot_patterns",
    author = "John Carr",
    author_email = "john.carr@unrouted.co.uk",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'buildbot',
    ],
)
