
from akit.testing.testjob import TestJob

class SettingsJob(TestJob):

    # Friendly name for the test job
    name = "Example Job"

    # Description of the job
    description = "This is an example job.  This discription describes the aspects of the job."

    # The test packs or tests that are included in this TestJob
    includes = [
        "tests.settings.systemsettings"
    ]

    # The tests that are to be excluded from this TestJob
    excludes = None
