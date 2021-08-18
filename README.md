# How to run dependency application

You have to download from the github and install with:

```
pip install .
```

Then, you could run with this command:

```
python -m dependency -c
```

And enter the command. Or you could write a script as the test file, and run the following command:

```
python -m dependency -s tests/test_input.txt
```

Or you could run the test, with pytest command.

```
pytest -v
```
