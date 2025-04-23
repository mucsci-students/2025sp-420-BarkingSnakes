# Filename: pytest.py
# Authors: John Hershey
# Creation Date 2025-04-22. Last Edit Date: 2025-04-22
# Description: execution class for running pytest code
# allows for adjustment of code coverage fail_under value if test coverage increases

import pytest
# set args to run on pytest
args = ["--cov", "--cov-report", "xml"]
pytest.main(args)

with open("coverage.xml", "r") as cov:
    # access coverage file
    data = cov.read()
    # get index of the current code coverage value
    ind = data.index("line-rate=")
    # access the current code coverage percentage
    newpercent = data[ind+13:ind+15]
    
with open(".coveragerc", "r") as currcov:
    # read coveragerc file
    covdata = currcov.read()
    # get index of current fail rate percentage
    ind2 = covdata.index("fail_under =")
    #access the current code coverage failure rate
    oldpercent = covdata[ind2+13:ind2+15]
    #if code coverage has increased adjust the fail rate in the coverage file
    if oldpercent < newpercent:
        with open(".coveragerc", "w") as newcov:
            #update the coverage file using the index of the fail-under field
            newcov.write(covdata[:ind2 + 13] + newpercent + covdata[ind2 + 15:])