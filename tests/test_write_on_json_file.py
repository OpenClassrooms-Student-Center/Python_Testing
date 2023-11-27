from server import write_on_json_file
import json
import os


def test_write_on_json_file():
    """
    Test the write_on_json_file function.

    This test case creates a temporary file for testing, calls the
    write_on_json_file function, checks the content of the file, and finally
    removes the temporary file.

    The test checks if the function successfully writes the specified
    key-value pair to the JSON file.
    """
    temp_file = "temp_test_file.json"

    try:
        write_on_json_file(temp_file, "key", "value")
        with open(temp_file, "r") as f:
            content = json.load(f)

        assert content == {"key": "value"}
    finally:
        os.remove(temp_file)


def test_write_on_json_file_update():
    """
    Test the update functionality of the write_on_json_file function.

    This test case creates a temporary file with existing data, calls the
    write_on_json_file function to update the file, checks the updated content
    of the file, and finally removes the temporary file.

    The test verifies that the function successfully updates the existing
    JSON file by adding a new key-value pair.
    """
    temp_file = "temp_test_file.json"

    try:
        existing_data = {"existing_key": "existing_value"}
        with open(temp_file, "w") as f:
            json.dump(existing_data, f)

        write_on_json_file(temp_file, "new_key", "new_value")
        with open(temp_file, "r") as f:
            content = json.load(f)

        assert content == {"new_key": "new_value"}

    finally:
        os.remove(temp_file)
