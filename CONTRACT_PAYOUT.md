# Logic-Sig Contract Account: A Factoring Game

This demo shows how you can use a Logic Signatures to payout "bounties" as rewards for
solving a problem. The problem isn't realistically very difficult, but
one can imagine a teacher modifying this game to give out ASA's / NFT's as student
rewards, or a crypto foundation paying out real rewards for finding very large primes (ok, that last one is a bit of a stretch, as the logic sig would
probably run out of budget trying to verify it...).

## Steps for reproducing
Assumes you've got the same setup as described in [The PyTeal Course](https://github.com/algorand-devrel/pyteal-course)

### Part I: Set up the local repo and sandbox:

1. Create a repo under the new directory **contract-accounts** with `git clone git@github.com:tzaffi/pyteal-course.git contract-accounts`
2. Modify the sandbox'es `docker-compose` as explained in [The PyTeal Course](https://github.com/algorand-devrel/pyteal-course) but make sure the `volumes:` is set to **bind** _source_ `path/to/contract-accounts` and _target_ `/data`
3. Bring up this sandbox with something like `./sandbox up dev`

### Part II: Compile the PyTeal Logic-Sig Contract-Account

4. `cd contract-accounts`
5. Configure the standard python virtual env as follows (slightly different on a Windows PC):
```sh
❯ python3 -m venv venv
❯ source ./venv/bin/activate
❯ pip3 install -r requirements.txt
```
6. Create a build directory with `mkdir build`
7. Now let's compile a Logic-Sig that pays out 10 Algo's whenever a caller solves an algebraic puzzle. The program is defined in [factorizer_game.py](./contracts/lsigs/factorizer_game.py) which is compiled using the python script [create_signature.py](./create_signature.py). (If you're curious, a unique contract-account is created for each parameter triple `a`, `p`, `q`, which determine the quadratic polynomial that needs to be factored for payout. In fact, `p` and `q` are the factor solutions).
Let's create this contract for parameters 1, 5, 7. Note that the output actually gives the contract-account's address. This is the address that should be funded so payouts can occur.
```sh
❯ python ./create_signature.py ./build contracts.lsigs.factorizer_game 1 5 7
contract: contracts.lsigs.factorizer_game
contract_args: ['1', '5', '7']
file name: factorizer_game_1_5_7
Logic Signature Address: PZBHMI3WNNU65SIFFAYT53UZKRQR4JGE3W7PCPYE3FQMENJTE6GU7YCMBE
```


### Part III: Running the Contract-Account

8. Enter the sandbox'es **algod** with something like `./sandbox enter algod`. This should bring you into the container and create a prompt such as:
```sh
root@6bafe6878810:~/testnetwork/Node#
```
9. In the algod shell: `cd /data` and make sure that `cat build/factorizer_game_1_5_7.teal` lists out the program compiled in step 7.
10. List out the available accounts (these should be avaiable in the default wallet for funding purpose) and set one of them as the funder and another as winner. EG:
```sh
# goal account list
[online]	KXMEH6DVK7HMTSWV27IDFCDVHIPUWJH5VZSLRJRJRCWAF5CDYZTNSUT3OE	KXMEH6DVK7HMTSWV27IDFCDVHIPUWJH5VZSLRJRJRCWAF5CDYZTNSUT3OE	2000000000000000 microAlgos
[online]	V56ACOZTFTGL5DUR7UNS5UBMYIEGKJ4Q7ZX2BT4DLOU4ODOSGVD2VJ2S6Q	V56ACOZTFTGL5DUR7UNS5UBMYIEGKJ4Q7ZX2BT4DLOU4ODOSGVD2VJ2S6Q	4000000000000000 microAlgos
[online]	WUCXRKKNIGQQY5BBYKMORALV5EHXTS5BGAI664VEFUTADP5YJ3OP7KUKFM	WUCXRKKNIGQQY5BBYKMORALV5EHXTS5BGAI664VEFUTADP5YJ3OP7KUKFM	4000000000000000 microAlgos
# FUNDER=KXMEH6DVK7HMTSWV27IDFCDVHIPUWJH5VZSLRJRJRCWAF5CDYZTNSUT3OE
# WINNER=WUCXRKKNIGQQY5BBYKMORALV5EHXTS5BGAI664VEFUTADP5YJ3OP7KUKFM
```
More succinctly:
```sh
FUNDER=`goal account list | head -n 1 | awk '{print $2}'`
WINNER=`goal account list | tail -n 1 | awk '{print $2}'`
```
Verify that this worked with `echo "$FUNDER and $WINNER"`

11. Let's also set up the lsig contract account address (recall we got this from step 7 above)x. EG with `PUZZLE=PZBHMI3WNNU65SIFFAYT53UZKRQR4JGE3W7PCPYE3FQMENJTE6GU7YCMBE` and make sure this worked with `echo $PUZZLE`
12. Let's have the funder send 100 Algo's over to our contract account: `goal clerk send -a 100000000 -f $FUNDER -t $PUZZLE`. Verify this worked with `goal account balance -a $PUZZLE`
13. Now let's try and solve the puzzle sending the prize money over to our winner. Before we proceed, make note of the winner's pre-puzzle balance:
`goal account balance -a $WINNER`
14. In order to solve the puzzle we'll need to encode the solutions `5` and `7` in base64. Let's do this as follows:
```sh
# echo 5 | python3 -c "import sys;import base64;print(base64.b64encode(int(sys.stdin.read()).to_bytes(8,'big')).decode('ascii'))"
AAAAAAAAAAU=
# echo 7 | python3 -c "import sys;import base64;print(base64.b64encode(int(sys.stdin.read()).to_bytes(8,'big')).decode('ascii'))"
AAAAAAAAAAc=
```
15. Now we're ready to try and solve the puzzle. Notice that we specify the prize amount (10 million Algos) along with the encoded arguments.
We specify the contrat account's program rather than its address (that would be cheating!!!!):
```sh
# goal clerk send -a 10000000 -t $WINNER --from-program build/factorizer_game_1_5_7.teal --argb64 "AAAAAAAAAAU=" --argb64 "AAAAAAAAAAc="
Sent 10000000 MicroAlgos from account PZBHMI3WNNU65SIFFAYT53UZKRQR4JGE3W7PCPYE3FQMENJTE6GU7YCMBE to address WUCXRKKNIGQQY5BBYKMORALV5EHXTS5BGAI664VEFUTADP5YJ3OP7KUKFM, transaction ID: WWX3WAGXNOXT3TLQGVUVUHLR6SRB352UI2FXL44SKA4RAXFK3ICA. Fee set to 1000
Transaction WWX3WAGXNOXT3TLQGVUVUHLR6SRB352UI2FXL44SKA4RAXFK3ICA committed in round 3
```
16. Verify the new balance of the winner with `goal account balance -a $WINNER`
17. Also verify that 10 million Algos plus the fee have been deducted from the contract address with `goal account balance -a $PUZZLE`
18. **Exercise for the reader**: What happens if we provide the wrong solution 0 (i.e. `AAAAAAAAAAA=`) and 1 (i.e. `AAAAAAAAAAE`)? Or what if we specify the wrong prize money
10000001?


