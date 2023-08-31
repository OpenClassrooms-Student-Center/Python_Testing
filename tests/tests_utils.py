import html


def decode_response(response_bytes):
    decoded_text = response_bytes.decode("utf-8")
    decoded_text = html.unescape(decoded_text)
    return decoded_text
