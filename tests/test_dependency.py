import os
from unittest import TestCase
from dependency.main import Dependency

class DependencyTest(TestCase):
    def setUp(self):
        with open(Dependency._dependency_file, "w") as file:
            file.write("")

    def test_depend(self):
        data = [
            "DEPEND TELNET TCPIP  NETCARD   ", 
            "DEPEND TCPIP  NETCARD ", 
            "DEPEND DNS TCPIP   NETCARD   ", 
            "DEPEND BROWSER   TCPIP HTML   ", 
            "INSTALL NETCARD", 
            "INSTALL TELNET", 
            "INSTALL foo",
            "REMOVE NETCARD",
            "INSTALL BROWSER", 
            "INSTALL DNS "
            ]
        expected = [
            "DEPEND TELNET TCPIP NETCARD",
            "DEPEND TCPIP NETCARD",
            "DEPEND DNS TCPIP NETCARD",
            "DEPEND BROWSER TCPIP HTML",
            "INSTALL NETCARD\n   NETCARD successfully installed", 
            "INSTALL TELNET\n   TCPIP successfully installed\n   TELNET successfully installed",
            "INSTALL foo\n   foo successfully installed",
            "REMOVE NETCARD\n   NETCARD is still needed",
            "INSTALL BROWSER\n   HTML successfully installed\n   BROWSER successfully installed", 
            "INSTALL DNS\n   DNS successfully installed"
        ]
        _output = Dependency(data).play()
        print(_output)
        for idx in range(len(_output)):
            assert _output[idx] == expected[idx]
        
        list_data = [
            "LIST"
            ]
        list_expected_1 = ["LIST", "HTML",  "BROWSER",   "DNS",   "NETCARD",   "foo",   "TCPIP", "TELNET"]
        _output = Dependency(list_data).play()
        for _e in list_expected_1:
            assert _e in _output[0]

        data_2 = [
            "REMOVE TELNET", 
            "REMOVE NETCARD",
            "REMOVE DNS", 
            "REMOVE NETCARD",
            "INSTALL foo",
            "INSTALL NETCARD ",
            "REMOVE TCPIP",
            "REMOVE BROWSER",
            "REMOVE TCPIP"
        ]
        expected_2 = [
            "REMOVE TELNET\n   TELNET successfully removed", 
            "REMOVE NETCARD\n   NETCARD is still needed", 
            "REMOVE DNS\n   DNS successfully removed", 
            "REMOVE NETCARD\n   NETCARD is still needed",
            "INSTALL foo\n   foo is already installed",
            "INSTALL NETCARD\n   NETCARD is already installed",
            "REMOVE TCPIP\n   TCPIP is still needed",
            "REMOVE BROWSER\n   BROWSER successfully removed\n   TCPIP is no longer needed\n   TCPIP successfully removed\n   NETCARD is no longer needed\n   NETCARD successfully removed\n   HTML is no longer needed\n   HTML successfully removed",
            "REMOVE TCPIP\n   TCPIP is not installed"
        ]
        _output = Dependency(data_2).play()
        for idx in range(len(_output)):
            assert _output[idx] == expected_2[idx]

        list_data_2 = ["LIST", "END"]
        list_expected_2 = ["LIST", "foo"]
        _output = Dependency(list_data_2).play()
        for _e in list_expected_2:
            assert _e in _output[0]
        assert "END" == _output[1]
    
    def test_input_1(self):
        os.system("python3 -m dependency -s tests/test_input.txt > test.txt")

        with open("test.txt", "r") as file:
            data = file.read()

        with open("tests/test_output.txt", "r") as file:
            _data = file.read()
        os.system("rm -f test.txt")
        assert data == _data
    
