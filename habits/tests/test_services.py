from unittest.mock import patch
from habits.services import send_telegram_message


@patch("habits.services.requests.post")
@patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "test_token"})
def test_send_telegram_message(self, mock_post):
    send_telegram_message(chat_id=12345, text="Test message")
    mock_post.assert_called_once_with(
        "https://api.telegram.org/bottest_token/sendMessage",
        data={"chat_id": 12345, "text": "Test message"},
    )
