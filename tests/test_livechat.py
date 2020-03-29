import pytest


@pytest.fixture
def delete_agents_managers(logged_rocket):
    for agent_id in ['agent1', 'agent2', 'manager1']:
        logged_rocket.livechat_remove_user(id=agent_id, user_type="agent")
        agent1_exists = logged_rocket.users_info(
            username=agent_id).json().get('success')
        if agent1_exists:
            user_id = logged_rocket.users_info(
                username=agent_id).json().get('user').get('_id')
            logged_rocket.users_delete(user_id)


@pytest.fixture
def test_new_visitor(logged_rocket, delete_agents_managers):
    new_visitor = logged_rocket.livechat_register_visitor(
        token='new-visitor-token').json()
    assert new_visitor['success']
    return new_visitor


def test_livechat_get_visitor_by_token(logged_rocket, test_new_visitor):
    visitor = logged_rocket.livechat_get_visitor_by_token(
        token='new-visitor-token').json()
    assert visitor['visitor']['_id'] == test_new_visitor['visitor']['_id']


@pytest.fixture
def agent1(logged_rocket):
    new_user = logged_rocket.users_create(email='agent1@domain.com', name='agent1', password='agent1',
                                          username='agent1').json()
    assert new_user['success']
    new_agent = logged_rocket.livechat_add_user(
        username="agent1", user_type="agent").json()
    assert new_agent['success']
    return new_agent


@pytest.fixture
def agent2(logged_rocket):
    new_user = logged_rocket.users_create(email='agent2@domain.com', name='agent2', password='agent2',
                                          username='agent2').json()
    assert new_user['success']
    new_agent = logged_rocket.livechat_add_user(
        username="agent2", user_type="agent").json()
    assert new_agent['success']
    return new_agent


def test_livechat_list_agent(logged_rocket, agent1, agent2):
    list_agent_get = logged_rocket.livechat_list_agents().json()
    assert list_agent_get['success']
    print(list_agent_get)
    assert agent1['user']['_id'] in [u['_id'] for u in list_agent_get['users']]
    assert agent2['user']['_id'] in [u['_id'] for u in list_agent_get['users']]


def test_livechat_add_manager(logged_rocket):
    manager1 = logged_rocket.users_create(email='manager1@domain.com', name='manager1', password='manager1',
                                          username='manager1').json()
    assert manager1['success']
    new_manager = logged_rocket.livechat_add_user(
        username="manager1", user_type="manager").json()
    assert new_manager['success']


def test_livechat_list_manager(logged_rocket):
    list_manager_get = logged_rocket.livechat_list_managers().json()
    assert list_manager_get['success']
    assert 'manager1' in [u['username'] for u in list_manager_get['users']]
