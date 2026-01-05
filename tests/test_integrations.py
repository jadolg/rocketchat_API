from uuid import uuid1

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketUnsuportedIntegrationType,
)

GENERAL_CHANNEL = "#general"


@pytest.fixture(autouse=True)
def integrations_create_webhook_incoming(logged_rocket):
    return logged_rocket.integrations_create(
        integrations_type="webhook-incoming",
        name=str(uuid1()),
        enabled=True,
        username=logged_rocket.me().get("username"),
        channel=GENERAL_CHANNEL,
        script_enabled=False,
    )


def test_integrations_create(integrations_create_webhook_incoming, logged_rocket):
    integration_webhook_outgoing = logged_rocket.integrations_create(
        integrations_type="webhook-outgoing",
        name=str(uuid1()),
        enabled=True,
        event="sendMessage",
        username=logged_rocket.me().get("username"),
        urls=["https://example.com/fake"],
        channel=GENERAL_CHANNEL,
        script_enabled=False,
    )
    assert "integration" in integration_webhook_outgoing


def test_integrations_get(integrations_create_webhook_incoming, logged_rocket):
    integration_id = integrations_create_webhook_incoming.get("integration").get("_id")
    logged_rocket.integrations_get(integration_id)


def test_integrations_history(integrations_create_webhook_incoming, logged_rocket):
    integration_id = integrations_create_webhook_incoming.get("integration").get("_id")
    logged_rocket.integrations_history(integration_id=integration_id)


def test_integrations_list(logged_rocket):
    iterated_integrations = list(logged_rocket.integrations_list())
    for integration in iterated_integrations:
        assert "_id" in integration


def test_integrations_remove(integrations_create_webhook_incoming, logged_rocket):
    integration = integrations_create_webhook_incoming.get("integration")
    logged_rocket.integrations_remove(integration.get("type"), integration.get("_id"))


def test_integrations_update(integrations_create_webhook_incoming, logged_rocket):
    integration_id = integrations_create_webhook_incoming.get("integration").get("_id")

    logged_rocket.integrations_update(
        integrations_type="webhook-incoming",
        name=str(uuid1()),
        enabled=False,
        username=logged_rocket.me().get("username"),
        channel=GENERAL_CHANNEL,
        script_enabled=False,
        integration_id=integration_id,
    )


def test_integration_invalid_type(logged_rocket):
    with pytest.raises(RocketUnsuportedIntegrationType):
        logged_rocket.integrations_create(
            integrations_type="not-valid-type",
            name=str(uuid1()),
            enabled=True,
            username=logged_rocket.me().get("username"),
            channel=GENERAL_CHANNEL,
            script_enabled=False,
        )
