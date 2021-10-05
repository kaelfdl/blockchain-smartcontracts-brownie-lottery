import pytest
from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import LOCAL_BLOCKCHAIN_ENV, fund_with_link, get_account


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Act
    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    tx.wait(20)  # Approximately 20 confirmations to calculate winner
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
