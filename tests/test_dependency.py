from unittest import TestCase
from dependency.main import Dependency

#class DependencyTest(TestCase):

def test_depend():
    data = [
        "DEPEND TELNET TCPIP  NETCARD   ", 
        "DEPEND TCPIP  NETCARD ", 
        "DEPEND DNS TCPIP   NETCARD   ", 
        "DEPEND BROWSER   TCPIP HTML   ", 
        ]
    expected = [
        "DEPEND TELNET TCPIP NETCARD",
        "DEPEND TCPIP NETCARD",
        "DEPEND DNS TCPIP NETCARD",
        "DEPEND BROWSER TCPIP HTML"
    ]
    _output = Dependency(data).play()
    for idx in range(len(_output)):
        assert _output[idx] == expected[idx]
        
def test_install():
    data = ["INSTALL NETCARD", "INSTALL TELNET"]
    expected = [
        "INSTALL NETCARD\n   NETCARD successfully installed",
        "INSTALL TELNET\n   TCPIP successfully installed\n  TELNET successfully installed"
        ]
    _output = Dependency(data).play()
    print(_output)
    for idx in range(len(data)):
        assert data[idx] == expected[idx]

def test_input_1():
    with open("tests/test_input.txt", "r") as file:
        data = file.read()
    lines = data.split("\n")
    response = Dependency(lines)

    with open("tests/test_output.txt", "r") as file:
        _data = file.read()
    
def test_package_object():
    data = '{"depend": ["{\\"depend\\": [\\"{\\\\\\"depend\\\\\\": [], \\\\\\"_id\\\\\\": \\\\\\"dfba3fb9-48c9-4caf-b425-faf5894d8e86\\\\\\", \\\\\\"name\\\\\\": \\\\\\"INTERNET\\\\\\"}\\"], \\"_id\\": \\"c4c22746-b7af-40ea-b9fe-d0e9525581d8\\", \\"name\\": \\"TCP\\"}"], "_id": "9c884bb1-8935-44c4-bc93-5880e4f46c21", "name": "BROWSER"}'

if "__main__" == __name__:
    test_depend()
    test_install()