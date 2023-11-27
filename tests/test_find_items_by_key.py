from server import find_items_by_key


def test_find_items_by_key_found(clubs):
    """
    Test the find_items_by_key function when searching for items with a
    specific key-value pair.

    This test checks the behavior of the find_items_by_key function when
    searching for items in a list that match a specific key-value pair.

    The expected result is a list containing the items that match the
    specified key and value.

    Args:
    - clubs (dict): A dictionary containing a list of clubs for testing.
    """
    result = find_items_by_key(
        items_list=clubs["clubs"], key="name", value="Iron Temple"
    )
    assert result == [
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        }
    ]


def test_find_items_by_key_not_found(clubs):
    """
    Test the find_items_by_key function when searching for items with a
    specific key-value pair that does not exist.

    This test checks the behavior of the find_items_by_key function when
    searching for items in a list that do not match a specific key-value pair.

    The expected result is None, indicating that no items were found.

    Args:
    - clubs (dict): A dictionary containing a list of clubs for testing.
    """
    result = find_items_by_key(
        items_list=clubs["clubs"], key="name", value="Nonexistent Club"
    )
    assert result is None


def test_find_items_by_key_empty_list():
    """
    Test the find_items_by_key function when searching in an empty list.

    This test checks the behavior of the find_items_by_key function when
    attempting to search for items in an empty list. The expected result is
    None, indicating that no items were found.
    """
    items_list = []
    result = find_items_by_key(
        items_list=items_list, key="name", value="item1"
    )
    assert result is None


def test_find_items_by_key_multiple_matches(clubs):
    """
    Test the find_items_by_key function when multiple items match the search
    criteria.

    This test checks the behavior of the find_items_by_key function when
    there are multiple items in the list that match the specified key: value.
    The expected result is a list containing all the matching items.

    Args:
    - clubs (dict): A dictionary containing a list of clubs for testing.
    """
    result = find_items_by_key(
        items_list=clubs["clubs"], key="name", value="Simply Lift"
    )
    assert result == [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        }
    ]
