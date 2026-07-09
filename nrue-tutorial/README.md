# OAI nrUE tutorial helper

This folder contains a small, non-invasive helper bundle for the official OAI 5G NR SA tutorial for nrUE.

Reference:
- https://github.com/openairinterface/openairinterface5g/blob/develop/doc/NR_SA_Tutorial_OAI_nrUE.md

## What is included
- A concise checklist based on the official tutorial
- Helper shell scripts for prerequisites, build, and RFsim execution

## Suggested workflow
1. Install the required host packages.
2. Build the OAI gNB and nrUE targets.
3. Start OAI CN5G and the gNB.
4. Run the nrUE helper script for RFsim or USRP.

## Helper scripts
- scripts/install-prerequisites.sh
- scripts/build-nrue.sh
- scripts/run-nrue-rfsim.sh

## Notes
- These files are additive only; existing OAI source files are left unchanged.
- Review the official tutorial for hardware-specific commands before using USRP hardware.
