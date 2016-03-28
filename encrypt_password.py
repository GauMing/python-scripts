#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

import gen_random_key

__author__ = 'Kohaku'

'''
encrypt and validate password
'''


def encrypt_password(raw_password, salt=None):
    if not salt:
        salt = gen_random_key.random_key(1, 8).pop()
    result = hashlib.sha256(salt + raw_password).hexdigest()
    return salt + result


def validate_password(encrypted, input_password):
    return encrypted == encrypt_password(input_password, encrypted[:8])


print validate_password(encrypt_password('hello'), 'hello')
