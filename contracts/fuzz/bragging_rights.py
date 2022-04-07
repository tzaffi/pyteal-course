# WARNING: this contract is for demo purposes only. It is NOT SAFE for production usage.

from pyteal import *
from pyteal import acct

MIN_PYMNT = Int(1)


def approval(collector_address: str):
    sender_idx = Int(0)
    receiver_idx = Int(1)
    is_rich = acct.AccountParam.balance(sender_idx) >= Int(100)


def clear():
    return Approve()
