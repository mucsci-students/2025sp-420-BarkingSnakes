# Filename: usertests.py
# Authors: John Hershey
# Creation Date 2025-04-24. Last Edit Date: 2025-04-24
# Description: pytest script for user to run tests and see coverage without extra args

import pytest
# set args to run on pytest
args = ["--cov", "--cov-report", "term-missing"]
pytest.main(args)
