import subprocess
import yaml

from sem3.checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_step1(self, make_bad_arx):
        # test1 output from archive
        result1 = checkout_negative(
            "cd {}; 7z e bad_arx -t{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "ERROR")
        assert result1, "test1 FAIL"

    def test_step2(self):
        # test2 full archive
        assert checkout_negative("cd {}; 7z t bad_arx.{}".format(data["folder_out"], data["type"]),
                                 "ERROR"), "test2 FAIL"
