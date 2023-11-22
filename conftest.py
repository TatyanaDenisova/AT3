import string
import random
import pytest
import yaml
from datetime import datetime

from sem3.checkers import checkout, getout

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return checkout(
        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]),
        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_off_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename,
                                                                                           data["bs"]), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture(autouse=True, scope="class")
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"],
                                                        data["folder_ext2"]), "")


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
             "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                            data["count"], data["bs"], stat), "")
