from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENV
from web3 import Web3

def deploy_fund_me():
    account = get_account()
    # publish_source = True means that will verify contract with etherscan
    
    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address  # uses most recently deployed MockV3Aggregator

    # .deploy needs a from key cause it is making a state change to the blockchain
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print((f"Contract deployed to {fund_me.address}"))
    return fund_me
    
    
def main():
    deploy_fund_me()