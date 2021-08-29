import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/wonders_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS2")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()


st.title("Seven Wonders NFT Appraisal System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Site Token Owner", options=accounts)
st.markdown("---")

################################################################################
# Register New Site
################################################################################
st.markdown("## Register new Site")
site_name = st.text_input("Enter the name of the Site")
perks = st.text_input("Enter the descriptions of perks of the Token")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
site_uri = st.text_input("Enter the URI to the Site")
if st.button("Register Site"):
    tx_hash = contract.functions.registerSite(
        address,
        site_name,
        perks,
        int(initial_appraisal_value),
        site_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display a Seven Wonders Site Token")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Seven Wonders Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)


################################################################################
# Appraise Token
################################################################################
st.markdown("## Appraise Tokens")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose a Site Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
report_uri = st.text_area("Enter notes about the appraisal")
if st.button("Appraise Token"):

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the appraisal report history")
site_token_id = st.number_input("Site ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": site_token_id}
    )
    appraisals = appraisal_filter.get_all_entries()
    if appraisals:
        for appraisal in appraisals:
            report_dictionary = dict(appraisal)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Appraisal Report Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This site token has no new appraisals")
