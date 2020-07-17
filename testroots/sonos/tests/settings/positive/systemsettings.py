
from sonos.testpacks.settings.settingstestpack import SettingsTestPack

from akit.testing.testcontainer import PositiveTestContainer

class PositiveSettingsTests(PositiveTestContainer, SettingsTestPack):

    def test_hello_world_b(self):
        print("Hello World, B")
        return
