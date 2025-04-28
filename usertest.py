# Filename: usertests.py
# Authors: John Hershey
# Creation Date 2025-04-24. Last Edit Date: 2025-04-25
# Description: pytest script for user to run tests and update coverage requirements
import pytest
import os
import sys

#run pytest
args =  ["--cov", "--cov-report", "xml", "--cov-report", "term-missing"]
pytest_result = pytest.main(args)
print("PYTEST EXIT CODE:", pytest_result, pytest_result.value)

# access current project coverage rate
with open("coverage.xml", "r") as cov:
    # access coverage file
    data = cov.read()
    # get index of the current code coverage value
    ind = data.index("line-rate=")
    # access the current code coverage percentage
    newpercent = int(float(data[ind + 11 : ind + 16]) * 100)
    
# update coveragerc required coverage
with open(".coveragerc", "r") as currcov:
    # read coveragerc file
    covdata = currcov.read()
    # get index of current fail rate percentage
    ind2 = covdata.index("fail_under =")
    #access the current code coverage failure rate
    curpercent = int(covdata[ind2 + 13 : ind2 + 16])
    #if code coverage has increased adjust the fail rate in the coverage file
    if curpercent < newpercent:
        with open(".coveragerc", "w") as newcov:
            #update the coverage file using the index of the fail-under field
            newcov.write(covdata[:ind2 + 13] + str(newpercent) + covdata[ind2 + 16:])
        print(f"Coverage updated to {newpercent}%")
#get rid of old file    
os.remove("coverage.xml")

sys.exit(pytest_result.value)