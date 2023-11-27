from server import find_first_item_by_key


def test_find_first_item_by_key_found(clubs):
    """
    Test the find_first_item_by_key function when the key-value pair is found
    in the list.

    This test checks the behavior of the find_first_item_by_key function when
    searching for the first item in a list using a specified key-value pair,
    and the pair is found.

    The expected result is the dictionary representing the found item.

    Parameters:
    - clubs (dict): A dictionary containing a list of clubs to search.
    """
    result = find_first_item_by_key(
        items_list=clubs["clubs"], key="name", value="Iron Temple"
    )
    assert result == {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4",
    }


def test_find_first_item_by_key_not_found(clubs):
    """
    Test the find_first_item_by_key function when the key-value pair is not
    found in the list.

    This test checks the behavior of the find_first_item_by_key function when
    searching for the first item in a list using a specified key-value pair,
    and the pair is not found.

    The expected result is None, indicating that no item was found.

    Parameters:
    - clubs (dict): A dictionary containing a list of clubs to search.
    """
    result = find_first_item_by_key(
        items_list=clubs["clubs"], key="name", value="item4"
    )
    assert result is None


def test_find_first_item_by_key_empty_list():
    """
    Test the find_first_item_by_key function when the list is empty.

    This test checks the behavior of the find_first_item_by_key function when
    searching for the first item in an empty list using a specified key-value
    pair.

    The expected result is None, indicating that no item was found in the
    empty list.
    """
    items_list = []
    result = find_first_item_by_key(
        items_list=items_list, key="name", value="item1"
    )
    assert result is None


def test_find_first_item_by_key_other_key(clubs):
    """
    Test the find_first_item_by_key function when searching by a different key.

    This test checks the behavior of the find_first_item_by_key function when
    searching for the first item using a key other than the one specified in
    the test data.

    The expected result is the item with the specified value for the specified
    key.

    Args:
    - clubs (dict): A dictionary containing a list of clubs for testing.
    """
    result = find_first_item_by_key(
        items_list=clubs["clubs"], key="email", value="admin@irontemple.com"
    )
    assert result == {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4",
    }


def test_find_first_item_by_key_other_value(clubs):
    """
    Test the find_first_item_by_key function when searching by a different
    value.

    This test checks the behavior of the find_first_item_by_key function when
    searching for the first item using a different value for the specified key
    in the test data.

    The expected result is the item with the specified value for the specified
    key.

    Args:
    - clubs (dict): A dictionary containing a list of clubs for testing.

    Returns:
    - None
    """
    result = find_first_item_by_key(
        items_list=clubs["clubs"], key="points", value="4"
    )
    assert result == {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4",
    }
