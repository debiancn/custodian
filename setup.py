#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name="custodian",
      version="0.3",
      description="DebianCN Custodian archive toolkit",
      author="Boyuan Yang",
      author_email="073plan@gmail.com",
      url="https://github.com/debiancn/custodian",
      install_requires = [
          "debian",
          "apt",
      ],
      packages=find_packages(),
      entry_points = {
          'console_scripts': [
              'update-repo-metadata=custodian.update_repo_metadata:main',
          ],
      },
     )

