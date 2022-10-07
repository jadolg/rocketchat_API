from uuid import uuid1

import pytest


@pytest.fixture(autouse=True)
def integrations_create_webhook_incoming(logged_rocket):
    return logged_rocket.integrations_create(
        integrations_type="webhook-incoming",
        name=str(uuid1()),
        enabled=True,
        username=logged_rocket.me().json().get("username"),
        channel="#general",
        script_enabled=False,
    ).json()


def test_integrations_create(integrations_create_webhook_incoming, logged_rocket):
    integration_webhook_incoming = integrations_create_webhook_incoming
    assert integration_webhook_incoming.get("success")

    integration_webhook_outgoing = logged_rocket.integrations_create(
        integrations_type="webhook-outgoing",
        name=str(uuid1()),
        enabled=True,
        event="sendMessage",
        username=logged_rocket.me().json().get("username"),
        urls=["https://example.com/fake"],
        channel="#general",
        script_enabled=False,
    ).json()
    assert integration_webhook_outgoing.get("success")


def test_integrations_get(integrations_create_webhook_incoming, logged_rocket):
    integration_id = integrations_create_webhook_incoming.get("integration").get("_id")
    assert logged_rocket.integrations_get(integration_id).json().get("success")


def test_integrations_history(integrations_create_webhook_incoming, logged_rocket):
    integration_id = integrations_create_webhook_incoming.get("integration").get("_id")
    assert logged_rocket.integrations_history(integration_id).json().get("success")


def test_integrations_list(logged_rocket):
    assert logged_rocket.integrations_list().json().get("success")


def test_integrations_remove(integrations_create_webhook_incoming, logged_rocket):
    integration = integrations_create_webhook_incoming.get("integration")
    assert (
        logged_rocket.integrations_remove(
            integration.get("type"), integration.get("_id")
        )
        .json()
        .get("success")
    )


def test_integrations_update(integrations_create_webhook_incoming, logged_rocket):
    integration_id = integrations_create_webhook_incoming.get("integration").get("_id")
    assert (
        logged_rocket.integrations_update(
            integrations_type="webhook-incoming",
            name=str(uuid1()),
            enabled=False,
            username=logged_rocket.me().json().get("username"),
            channel="#general",
            script_enabled=False,
            integration_id=integration_id,
        )
        .json()
        .get("success")
    )
