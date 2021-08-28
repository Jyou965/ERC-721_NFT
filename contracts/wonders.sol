pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract WondersToken is ERC721Full {
    constructor() public ERC721Full("WondersToken", "WDRS") {}

    struct Site {
        string siteName;
        string perks;
        uint256 appraisalValue;
    }

    mapping(uint256 => Site) public siteCollection;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerSite(
        address owner,
        string memory siteName,
        string memory perks,
        uint256 initialAppraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        siteCollection[tokenId] = Site(siteName, perks, initialAppraisalValue);

        return tokenId;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) public returns (uint256) {
        siteCollection[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return siteCollection[tokenId].appraisalValue;
    }
}
