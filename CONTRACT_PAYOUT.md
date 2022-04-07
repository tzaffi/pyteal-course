# Logic-Sig Contract Account: A Factoring Game

This demo shows how you can use a Logic Signatures to payout "bounties" as rewards for
solving a problem. The problem isn't realistically very difficult, but
one can imagine a teacher modifying this game to give out ASA's / NFT's as student
rewards, or a crypto foundation paying out real rewards for finding very large primes.

## Steps for reproducing
Assumes you've got the same setup as described in [The PyTeal Course](https://github.com/algorand-devrel/pyteal-course)

1. Create a repo under the new directory **contract-accounts** with `git clone git@github.com:tzaffi/pyteal-course.git contract-accounts`
2. Modify the sandbox'es `docker-compose` as explained in [The PyTeal Course](https://github.com/algorand-devrel/pyteal-course) but make sure the `volumes:` is set to **bind** _source_ `path/to/contract-accounts` and _target_ `/data`
3. `cd contract-accounts`
4. Configure the standard python virtual env as in [The PyTeal Course](https://github.com/algorand-devrel/pyteal-course) step 5 + `pip3 install -r requirements.txt`. (If you are on Linux/Mac `make venv-reqs` should work)