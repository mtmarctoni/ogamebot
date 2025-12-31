import requests
from typing import Dict, Any, Optional


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str, verbose: bool = False):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.verbose = verbose

    def _post(self, method: str, data: Dict[str, Any]) -> Any:
        url = f"{self.base_url}/{method}"
        if self.verbose:
            print(f"[TelegramNotifier] POST {url}")
            print(f"[TelegramNotifier] Data: {data}")
        try:
            response = requests.post(url, data=data)
            if self.verbose:
                print(f"[TelegramNotifier] Status Code: {response.status_code}")
                print(f"[TelegramNotifier] Response Text: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if self.verbose:
                print(f"[TelegramNotifier] Exception: {e}")
            raise

    def send_message(self, text: str):
        data = {"chat_id": self.chat_id, "text": text}
        return self._post("sendMessage", data)

def safe_notify(notifier: Optional[TelegramNotifier], message: str) -> None:
    """
    Safely send a notification using the TelegramNotifier.
    If the notifier fails, log the error and continue execution.

    Args:
        notifier (Optional[TelegramNotifier]): The notifier instance.
        message (str): The message to send.
    """
    if notifier:
        try:
            notifier.send_message(message)
        except Exception as e:
            print(f"[ERROR] Notifier failed: {e}")