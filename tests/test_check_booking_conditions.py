from server import check_booking_conditions


class FlashRecorder:
    """
    A class for recording flash messages in a Flask application.

    This class can be used to record flash messages typically used in Flask
    applications for one request and response cycle.

    Attributes:
    - messages (list): A list to store the recorded flash messages.

    Methods:
    - __init__(): Initializes an instance of FlashRecorder with an empty list.
    - __call__(message): A callable method that appends a message to the list.
    - flash(message): Another method to append a message to the list.
    - get_messages(): Retrieves the recorded messages.
    """

    def __init__(self):
        """
        Initialize an instance of FlashRecorder.

        The messages attribute is set to an empty list.
        """
        self.messages = []

    def __call__(self, message):
        """
        Callable method to add a message to the list.

        Parameters:
        - message (str): The flash message to be recorded.
        """
        self.messages.append(message)

    def flash(self, message):
        """
        Add a message to the list.

        Parameters:
        - message (str): The flash message to be recorded.
        """
        self.messages.append(message)

    def get_messages(self):
        """
        Retrieve the recorded flash messages.

        Returns:
        - list: A list containing the recorded flash messages.
        """
        return self.messages


def test_check_booking_conditions_success():
    """
    Test the check_booking_conditions function for a successful booking.

    This test checks the behavior of the check_booking_conditions function when
    the booking conditions are successfully met. The conditions include having
    enough places available, sufficient points, and other parameters within the
    expected ranges.

    The expected result is True.

    Parameters:
    - places_required (int): The number of places requested for booking.
    - points (int): The current points of the user making the booking.
    - MAX_PLACES (int): The maximum number of places available for booking.
    - current_cart (int): The current number of places in the user's cart.
    - current_places_available (int): The current number of places available.
    - club (str): The name of the club for the booking.
    - competition (str): The name of the competition for the booking.
    """
    result = check_booking_conditions(
        places_required=5,
        points=10,
        MAX_PLACES=20,
        current_cart=0,
        current_places_available=15,
        club="Example Club",
        competition="Example Competition",
    )
    assert result is True


def test_check_booking_conditions_insufficient_points():
    """
    Test the check_booking_conditions function for insufficient points.

    This test checks the behavior of the check_booking_conditions function when
    the user has insufficient points for the requested booking. The conditions
    include having fewer points than required for the booking.

    The expected result is False, and the function should trigger a
    flash message indicating the lack of sufficient points.

    Parameters:
    - places_required (int): The number of places requested for booking.
    - points (int): The current points of the user making the booking.
    - MAX_PLACES (int): The maximum number of places available for booking.
    - current_cart (int): The current number of places in the user's cart.
    - current_places_available (int): The current number of places available.
    - club (str): The name of the club for the booking.
    - competition (str): The name of the competition for the booking.
    - flash_function (FlashRecorder): An instance of FlashRecorder to record
    flash messages.
    """
    flash_recorder = FlashRecorder()
    result = check_booking_conditions(
        places_required=20,
        points=5,
        MAX_PLACES=20,
        current_cart=0,
        current_places_available=15,
        club="Example Club",
        competition="Example Competition",
        flash_function=flash_recorder,
    )

    assert result is False
    assert (
        "Sorry, your club doesn't have enough points!"
        in flash_recorder.get_messages()
    )


def test_check_booking_conditions_exceeded_booking_limit():
    """
    Test the check_booking_conditions function for exceeded booking limit.

    This test checks the behavior of the check_booking_conditions function when
    the user's requested booking exceeds the maximum allowed places for a club.
    The conditions include having a total number of places (in the cart and
    requested) exceeding the maximum places available for a club.

    The expected result is False, and the function should trigger a flash
    message indicating that the booking limit has been exceeded.

    Parameters:
    - places_required (int): The number of places requested for booking.
    - points (int): The current points of the user making the booking.
    - MAX_PLACES (int): The maximum number of places available for booking.
    - current_cart (int): The current number of places in the user's cart.
    - current_places_available (int): The current number of places available.
    - club (str): The name of the club for the booking.
    - competition (str): The name of the competition for the booking.
    - flash_function (FlashRecorder): An instance of FlashRecorder to record
    flash messages.
    """
    flash_recorder = FlashRecorder()
    result = check_booking_conditions(
        places_required=10,
        points=15,
        MAX_PLACES=20,
        current_cart=15,
        current_places_available=5,
        club="Example Club",
        competition="Example Competition",
        flash_function=flash_recorder,
    )

    assert result is False
    assert (
        "Sorry, you have exceeded the booking limit!"
        in flash_recorder.get_messages()
    )


def test_check_booking_conditions_insufficient_available_places():
    """
    Test the check_booking_conditions function for insufficient available
    places.

    This test checks the behavior of the check_booking_conditions function when
    the user's requested booking exceeds the available places, considering both
    the places in the cart and the requested places.

    The expected result is False, and the function should trigger a flash
    message indicating that the booked places exceed the available places.

    Parameters:
    - places_required (int): The number of places requested for booking.
    - points (int): The current points of the user making the booking.
    - MAX_PLACES (int): The maximum number of places available for booking.
    - current_cart (int): The current number of places in the user's cart.
    - current_places_available (int): The current number of places available.
    - club (str): The name of the club for the booking.
    - competition (str): The name of the competition for the booking.
    - flash_function (FlashRecorder): An instance of FlashRecorder to record
    flash messages.
    """
    flash_recorder = FlashRecorder()
    result = check_booking_conditions(
        places_required=10,
        points=15,
        MAX_PLACES=20,
        current_cart=5,
        current_places_available=5,
        club="Example Club",
        competition="Example Competition",
        flash_function=flash_recorder,
    )

    assert result is False
    assert (
        "Sorry, you booked more places than available!"
        in flash_recorder.get_messages()
    )


def test_check_booking_conditions_exceeded_max_places():
    """
    Test the check_booking_conditions function for exceeding the maximum allowed places.

    This test checks the behavior of the check_booking_conditions function when
    the user's requested booking exceeds the maximum allowed places for a club.
    The conditions include having the number of places requested exceeding the
    maximum allowed places.

    The expected result is False, and the function should trigger a flash
    message indicating that the user can't book more than the maximum allowed places.

    Parameters:
    - places_required (int): The number of places requested for booking.
    - points (int): The current points of the user making the booking.
    - MAX_PLACES (int): The maximum number of places available for booking.
    - current_cart (int): The current number of places in the user's cart.
    - current_places_available (int): The current number of places available.
    - club (str): The name of the club for the booking.
    - competition (str): The name of the competition for the booking.
    - flash_function (FlashRecorder): An instance of FlashRecorder to record
    flash messages.
    """
    flash_recorder = FlashRecorder()
    print("Test - places_required:", 25)
    result = check_booking_conditions(
        places_required=25,
        points=40,
        MAX_PLACES=12,
        current_cart=0,
        current_places_available=5,
        club="Example Club",
        competition="Example Competition",
        flash_function=flash_recorder,
    )
    assert result is False
    print("Messages in flash_recorder:", flash_recorder.get_messages())
    assert (
        f"Sorry, you can't book more than {12} places!"
        in flash_recorder.get_messages()
    )


def test_flash_recorder_add_message():
    """
    Test the flash method of FlashRecorder.

    This test checks whether the flash method correctly adds a message to the list.

    Parameters:
    - message (str): The flash message to be recorded.
    """
    flash_recorder = FlashRecorder()
    message = "Test message"

    flash_recorder.flash(message)

    assert len(flash_recorder.get_messages()) == 1
    assert flash_recorder.get_messages()[0] == message
