# Filename: pytestscript.py
# Authors: John Hershey
# Creation Date 2025-04-22. Last Edit Date: 2025-04-24
# Description: execution class for actions to use to run pytest and update coverage
# NOT FOR USERS: users should use "usertests.py" for test coverage to avoid manipulating coveragerc
import pytest
    
# try to open the archived file
try:
    with open("../coverage.txt", "r") as f:
        oldmincov = int(f.read() or 0)
except FileNotFoundError:
    oldmincov = 80

# update coveragerc from the archived file
with open(".coveragerc", "r") as currcov:
    # read coveragerc file
    covdata = currcov.read()
    # get index of current fail rate percentage
    ind2 = covdata.index("fail_under =")
    #access the current code coverage failure rate
    curpercent = int(covdata[ind2 + 13 : ind2 + 16])
    #if code coverage has increased adjust the fail rate in the coverage file
    if curpercent < oldmincov:
        with open(".coveragerc", "w") as newcov:
            #update the coverage file using the index of the fail-under field
            newcov.write(covdata[:ind2 + 13] + str(oldmincov) + covdata[ind2 + 16:])

#run pytest
args =  ["--cov", "--cov-report", "xml"]
pytest.main(args)

# access current project coverage rate
with open("coverage.xml", "r") as cov:
    # access coverage file
    data = cov.read()
    # get index of the current code coverage value
    ind = data.index("line-rate=")
    # access the current code coverage percentage
    newpercent = int(float(data[ind + 11 : ind + 16]) * 100)

# if coverage has increased update archive file
if newpercent > oldmincov:
    with open("../coverage.txt", "w") as f:
        f.write(str(newpercent))
print(__file__)