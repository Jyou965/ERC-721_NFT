# seven_wonders_NFT

In this activity, you’ll create a dApp for the artwork token.

## Instructions

The instructions for this activity are divided into the following subsections:

1. Deploy the Contract

2. Prepare the Environment

3. Build the dApp

### Deploy the Contract

1. Create a new file in the Remix IDE, and then copy the code in the provided `artwork.sol` file into the new file. Spend a few moments reviewing the code.

2. Launch a Quickstart blockchain with Ganache, and then use MetaMask and the Remix IDE to compile and deploy the `ArtToken` contract.

    > **Hint** The previous module has a detailed video about deploying contracts with Ganache, MetaMask, and the Remix IDE that you can reference for this contract.

### Prepare the Environment

Copy the provided `SAMPLE.env` file to a new file named `.env`, and then add the missing data to the environment variables.

> **Hint** You can find the value for `WEB3_PROVIDER_URI`  in the RPC Server field in Ganache. For the `SMART_CONTRACT_ADDRESS` value, use the address of the deployed contract in the Remix IDE. You can find it in the Deployed Contracts section.

### Build the dApp

1. Open `app.py` in the `Unsolved` folder.

2. In `app.py`, in the `load_contract` function, write the code to load the smart contract. To do so, complete the following substeps:

    * Use the following code to load the `artwork_abi.json` file that already exists in the `contracts/compiled` folder:

        ```python
        with open(Path('./contracts/compiled/artwork_abi.json')) as f:
            artwork_abi = json.load(f)
        ```

    * Use the following code to load the contract with Web3:

        ```python
        contract = w3.eth.contract(
            address=contract_address,
            abi=artwork_abi
        )
        ```

3. in the “Register New Artwork” section of code, write the code to register new artwork. To do so, complete the following substeps:

    * Define a new Streamlit component that gets the address of the artwork owner from the user. Use any Streamlit component that you’d like.

    * Define a new Streamlit component that gets the URI for the artwork. Have the user enter it as a string.

    * In the code for the Register Artwork button, use Web3 to send a transaction to the smart contract that registers the new artwork data based on the two preceding Streamlit components.

        > **Hint** Use the Web3 `transact` function to send the user data to the `registerArtwork` function in the contract.

4. In the “Display a Token” section of code, write the code to display a token. To do so, complete the following substeps:

    * Use Web3 to call the `ownerOf` function of the contract.

    * Use the `tokenURI` function of the contract to get the URI for the art token.

        > **Hint** You can find examples that use `ownerOf` and `tokenURI` on the [OpenZeppelin documentation page](https://docs.openzeppelin.com/contracts/2.x/api/token/erc721#IERC721-ownerOf-uint256-) or through an internet search.

5. Run the application by using `streamlit run app.py`. Test the functionality of the dApp to make sure that it works as expected.