import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

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

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_site(site_name, site_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(site_file.getvalue())

    # Build a token metadata file for the site
    token_json = {
        "name": site_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


st.title("Seven Wonders NFT Appraisal System")

# Title image
title_image = Image.open("Seven_Wonders_Photo.png")
st.write("")
st.image(title_image, width=643)
st.markdown("---")

st.markdown("## Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Site Token Owner", options=accounts)
st.markdown("---")

################################################################################
# Register New Site
################################################################################
st.markdown("## Register new site")
site_name = st.text_input("Enter the name of the Site")
perks = st.text_input("Enter the descriptions of perks of the Token")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
file = st.file_uploader("Upload New Site", type=["jpg", "jpeg", "png"])
if st.button("Register Site"):
    site_ipfs_hash = pin_site(site_name, file)
    site_uri = f"ipfs://{site_ipfs_hash}"
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
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Site IPFS Gateway Link](https://ipfs.io/ipfs/{site_ipfs_hash})")
    st.balloons()
st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display a Seven Wonders site token")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Seven Wonders Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the site token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the site token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)


################################################################################
# Appraise Token
################################################################################
st.markdown("## Appraise tokens")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose a Site Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
appraisal_report_content = st.text_area("Enter notes about the appraisal")
if st.button("Appraise Token"):

    # Use Pinata to pin an appraisal report for the report URI
    appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content)
    report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

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
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Appraisal Event Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This site token has no new appraisals")
st.markdown("---")
st.markdown("## By Team NFTerrific")

