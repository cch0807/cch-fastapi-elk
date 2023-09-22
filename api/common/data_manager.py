import random
import secrets
import string


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return "".join(secrets.choice(letters) for _ in range(length))


def generate_data_list(data_size):
    data_list: list = [
        {
            "id": i,
            "name": generate_random_string(10),
            "price": random.randint(100000, 1000001),
        }
        for i in range(data_size)
    ]

    return data_list


# def insert_data(index_name: str, data_size: int) -> str:
#     data_list = generate_data_list(data_size)
#     return data_list


if __name__ == "__main__":
    secure_random_string = generate_random_string(10)
    # print(secure_random_string)
