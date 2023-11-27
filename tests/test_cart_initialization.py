from server import cart_initialization


def test_cart_initialization(competitions, clubs):
    """
    Test the cart_initialization function.

    This test case checks if the cart_initialization function correctly
    initializes an empty cart with competitions as outer keys and clubs as
    inner keys, all set to zero.

    Returns:
    - None
    """

    # Call the function
    result = cart_initialization()

    # Verify that the result is a dictionary
    assert isinstance(result, dict)

    # Verify that competitions are outer keys
    for competition in competitions["competitions"]:
        assert competition["name"] in result.keys()

        # Verify that clubs are inner keys, all set to zero
        for club in clubs["clubs"]:
            assert result[competition["name"]][club["name"]] == 0
