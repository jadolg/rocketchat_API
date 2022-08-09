import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


@pytest.fixture(scope="module")
def recipient_user(create_user):
    _recipient = create_user(name="user1")

    return _recipient.name


@pytest.fixture(scope="module")
def recipient_user3(create_user):
    _recipient = create_user(name="user3", email="anotherone@domain.com")

    return _recipient.name


@pytest.fixture(scope="module")
def recipient_user2(create_user):
    _recipient = create_user(name="user2", email="another@domain.com")

    return _recipient.name


def test_im_create_multiple(logged_rocket, recipient_user3, recipient_user2):
    im_create = logged_rocket.im_create_multiple(
        [recipient_user3, recipient_user2]
    ).json()
    assert im_create.get("success")
    room_id = im_create.get("room").get("_id")
    im_send = logged_rocket.chat_post_message(
        room_id=room_id, text="Das ist eine Testnachricht"
    ).json()
    assert im_send.get("success")


def test_im_create(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    assert im_create.get("success")


def test_im_send(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_send = logged_rocket.chat_post_message(room_id=room_id, text="test").json()
    assert im_send.get("success")


def test_im_send_no_text(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_send = logged_rocket.chat_post_message(room_id=room_id, text=None).json()
    assert im_send.get("success")


def test_im_list(logged_rocket, recipient_user):
    logged_rocket.im_create(recipient_user)
    im_list = logged_rocket.im_list().json()
    assert im_list.get("success")


def test_im_close_open(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_close = logged_rocket.im_close(room_id).json()
    assert im_close.get("success")
    im_open = logged_rocket.im_open(room_id).json()
    assert im_open.get("success")


def test_im_set_topic(logged_rocket, recipient_user):
    topic = "this is my new topic"
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_set_topic = logged_rocket.im_set_topic(room_id, topic).json()
    assert im_set_topic.get("success")
    assert im_set_topic.get("topic") == topic, "Topic set does not match topic returned"


def test_im_list_everyone(logged_rocket):
    im_list_everyone = logged_rocket.im_list_everyone().json()
    assert im_list_everyone.get("success")


def test_im_history(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_history = logged_rocket.im_history(room_id).json()
    assert im_history.get("success")


def test_im_members(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_members = logged_rocket.im_members(room_id=room_id).json()
    assert im_members.get("success")
    assert im_members.get("members")[0].get("name") == "user1"


def test_im_messages(logged_rocket, recipient_user):
    im_message = logged_rocket.im_messages(username=recipient_user).json()
    assert im_message.get("success")
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_message = logged_rocket.im_messages(room_id=room_id).json()
    assert im_message.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.im_messages()


def test_im_messages_others(logged_rocket, recipient_user):
    # ToDo: Try changing the access configuration so endpoint can be successfully tested
    im_create = logged_rocket.im_create(recipient_user).json()
    room_id = im_create.get("room").get("_id")
    im_messages_others = logged_rocket.im_messages_others(room_id).json()
    assert not im_messages_others.get("success")


def test_im_files(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    assert im_create.get("success")

    im_files = logged_rocket.im_files(room_id=im_create.get("room").get("_id")).json()
    assert im_files.get("success")

    im_files = logged_rocket.im_files(user_name=recipient_user).json()
    assert im_files.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.im_files()


def test_im_counters(logged_rocket, recipient_user):
    im_create = logged_rocket.im_create(recipient_user).json()
    assert im_create.get("success")

    im_counters = logged_rocket.im_counters(
        room_id=im_create.get("room").get("_id")
    ).json()
    assert im_counters.get("success")

    im_counters = logged_rocket.im_counters(
        room_id=im_create.get("room").get("_id"),
        user_name=logged_rocket.me().json().get("_id"),
    ).json()
    assert im_counters.get("success")
