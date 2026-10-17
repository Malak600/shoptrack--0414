# BlockCert

**Blockchain certificate verification for an Istanbul Kültür University student club**

Course project for **SEN0401 Special Topics: Blockchain**, 2026–2027 Fall.

---

## The problem

The club sends its event and workshop certificates as PDF files. Anyone can edit a PDF or make a new one from the template, so employers and internship coordinators cannot tell a real certificate from a fake. The club also keeps no central record of what it has issued.

## The solution

BlockCert records a fingerprint (SHA-256 hash) of every certificate on a public blockchain.

1. A **club administrator** issues a certificate from the issuer dashboard.
2. The system builds the certificate as a JSON-LD document and validates it.
3. Its hash is stored on chain by the registry smart contract.
4. The **club member** receives the certificate file and a QR code.
5. A **verifier** (for example, an employer) scans the QR code or uploads the file and sees:
   - **Valid**: issued by the club and not revoked
   - **Revoked**: issued, then withdrawn by the club
   - **Unknown**: not issued by the club, or the file was edited

Only hashes go on chain, never names or student numbers, in line with KVKK (Law No. 6698).

## Architecture

```
┌────────────────────┐        ┌──────────────────────┐
│  Issuer dashboard  │        │ Verification portal  │
│ React + ethers.js  │        │ React + ethers.js    │
│ + MetaMask         │        │ + QR scanner         │
└─────────┬──────────┘        └──────────┬───────────┘
          │ issue / revoke                │ verify (read-only)
          ▼                               ▼
     ┌─────────────────────────────────────────┐
     │  CertificateRegistry smart contract     │
     │  Solidity · Ethereum Sepolia testnet    │
     │  hash → (issuer, issuedAt, revoked)     │
     └─────────────────────────────────────────┘
          ▲
          │ validate before hashing
┌─────────┴──────────┐
│ Validation service │
│ Python · RDFLib +  │
│ pySHACL            │
└────────────────────┘
```

## Repository structure

```
blockcert/
├── contracts/     Solidity contract, Hardhat tests and deploy scripts
├── dashboard/     Issuer dashboard (club administrators)
├── portal/        Public verification page
├── validator/     JSON-LD certificate schema, SHACL shape, Python validator
├── docs/          Diagrams, user guide, meeting notes
└── proposal/      Proposal files saved from the Proposal Workbench
```

## Tech stack

| Layer | Technology |
|---|---|
| Blockchain | Ethereum Sepolia testnet, Solidity, OpenZeppelin `Ownable` |
| Contract tooling | Hardhat |
| Front end | React, ethers.js, MetaMask |
| Certificate data | JSON-LD 1.1, PROV-O, W3C Verifiable Credentials model |
| Validation | SHACL, pySHACL, RDFLib (Python) |

## Smart contract interface (planned)

| Function | Who can call | What it does |
|---|---|---|
| `issue(bytes32 hash)` | Club issuer only | Registers one certificate |
| `batchIssue(bytes32[] hashes)` | Club issuer only | Registers many certificates at once |
| `revoke(bytes32 hash)` | Club issuer only | Marks a certificate as revoked |
| `verify(bytes32 hash)` | Anyone | Returns issued, revoked, issuer and timestamps |

## Getting started

> The code is not written yet; these steps will be completed as each part is built.

```bash
git clone https://github.com/<owner>/blockcert.git
cd blockcert/contracts
npm install
npx hardhat test
```

You will need Node.js 20+, Python 3.11+, MetaMask, and some Sepolia test ETH from a faucet.

## Team

| Member | Role | Owns |
|---|---|---|
| Malak Alfakavi | Team lead · smart contract · front end | Registry contract, issuer dashboard |
| Raghd Alfakavi | Back end · testing · release | Verification portal, tests, releases |

## Milestones

| Date | Milestone |
|---|---|
| 2026-10-24 | Proposal handed in, repository created, club meeting held |
| 2026-11-14 | Registry contract with unit tests deployed on Sepolia |
| 2026-11-28 | Issuer dashboard: single and batch issuing |
| 2026-12-12 | Verification portal with QR code; test report |
| 2026-12-19 | Release v1.0, validation with club members, final submission |

## How we work

- Each member commits from their **own GitHub account**.
- Work happens on branches and is merged into `main` through pull requests.
- Every work-log entry in the Proposal Workbench links the commit that shows the work.
- When the proposal is posted, the commit message carries the work log's fingerprint.

## License

MIT
