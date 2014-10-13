#/usr/bin/env bash
#
# Run static analysis of the codebase
#
# This is run on Travis to ensure that pull requests conform to the project coding standards.

# Ideally, this figure should be < 100.  I'll keep reducing it as the
# codebase gets tidied up incrementally.
THRESHOLD=10

# Some warnings aren't worth worrying about...
IGNORE="W292,E202,E128,E124"

# Run flake8 and convert the output into a format that the "violations" plugin
# for Jenkins/Hudson can understand.  Ignore warnings from migrations we we don't
# really care about those.
ERROR_FILE="violations.txt"
flake8 --ignore=$IGNORE accounting --exclude migrations | perl -ple "s/: /: [E] /" > $ERROR_FILE
cat $ERROR_FILE


# Check that the number of violations is acceptable
NUMERRORS=`cat $ERROR_FILE | wc -l`
if [ $NUMERRORS -gt $THRESHOLD ]
then
    echo "Too many flake8 errors - maximum allowed is $THRESHOLD, found $NUMERRORS"
    exit 1
fi
