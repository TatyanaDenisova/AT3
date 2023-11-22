import yaml
from sem3.checkers import checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive():

    def test_step1(self):
        # test1 create files to archive
        result1 = checkout("cd {}; 7z a {}/arx2 -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                           "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["folder_out"]), "arx2.{}".format(data["type"]))
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, make_files):
        # test2 output from archive
        result1 = checkout("cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]),
                           "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["folder_ext"]), make_files[0])
        assert result1 and result2, "test2 FAIL"

    def test_step3(self):
        # test3 full archive
        assert checkout("cd {}; 7z t arx2.{}".format(data["folder_out"], data["type"]),
                        "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4 renew archive
        assert checkout("cd {}; 7z u {}/arx2.{}".format(data["folder_in"], data["folder_out"], data["type"]),
                        "Everything is Ok"), "test4 FAIL"

    def test_step5(self):
        # test5 del files from archive
        assert checkout("cd {}; 7z d arx2.{}".format(data["folder_out"], data["type"]),
                        "Everything is Ok"), "test5 FAIL"

    def test_step6(self):
        # test6 show archive content
        assert checkout("cd {}; 7z l arx2.{}".format(data["folder_out"], data["type"]), "Listing archive"), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder):
        # test7 unpacing subfolder
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                            "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]),
                            "Everything is Ok"))
        for i in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), i))
        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test7 FAIL"
