import json


def load_user_data():
    try:
        with open("user_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading user data: {e}")
        data = {}
    return data


def save_user_data(data):
    try:
        with open("user_data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving user data: {e}")


user_data = load_user_data()


def update_user_data():
    save_user_data(user_data)
