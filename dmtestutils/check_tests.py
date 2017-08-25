#!/usr/bin/env python
"""
Script to be run after testing, to ensure that no test code has failed to run. Any missing
lines are a hard-fail for travis, where this script has been included in the build process.
"""
from coverage import coverage
from coverage.summary import SummaryReporter
import sys


ERROR_TEST_CODE_NOT_EXECUTED = 1
ERROR_NO_TEST_FILES = 2


def main():
    cov = coverage()
    cov.load()
    cov.config.from_args(include='tests/*')
    reporter = SummaryReporter(cov, cov.config)
    files = reporter.find_file_reporters(morfs=None)

    collect_missing = list()

    if files:
        for f in files:
            filename, statements, excluded, missing, missing_formatted = cov.analysis2(f)
            if missing:
                collect_missing.append((f.relative_filename(), missing_formatted))

        if collect_missing:
            sys.stderr.write("Some or all code lines in the following test modules are not being executed:\n")
            sys.stderr.write('\n'.join('{}\t{}'.format(*f) for f in collect_missing))
            sys.stderr.write('\n')
            return ERROR_TEST_CODE_NOT_EXECUTED

        return 0

    else:
        sys.stderr.write("Tests must have been run with --cov=tests in order to check coverage.\n")
        return ERROR_NO_TEST_FILES


sys.exit(main())
