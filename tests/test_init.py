# -*- coding: utf-8 -*-
"""
Tests for the module __init__ file.
"""
import os
import sys
import importlib
from unittest import mock

import mu


def test_gettext_translation():
    """
    Test the right translation is set based on the LC_ALL environmental
    variable.
    """
    if sys.platform == 'win32':
        # Unix only test.
        return
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'

    with mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['es_ES']


def test_defaultlocale_type_error():
    """
    Test that a TypeError in the locale.getdefaultlocale is detected and
    the translation language is set to English by default.
    """
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'
    mock_locale = mock.MagicMock(side_effect=TypeError('Ups'))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['en']


def test_defaultlocale_value_error():
    """
    Test that a ValueError is detected and the translation language is set
    to English by default.
    """
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'
    mock_locale = mock.MagicMock(side_effect=ValueError('Ups'))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['en']


def test_defaultlocale_empty_raises_value_error():
    """
    If no language code is detected, then raise a ValueError to cause it to
    default to 'en'.
    """
    old_lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'es_ES.UTF-8'
    mock_locale = mock.MagicMock(return_value=('', ''))

    with mock.patch('locale.getdefaultlocale', mock_locale), \
            mock.patch('gettext.translation') as translation:
        importlib.reload(mu)

    if old_lc_all:
        os.environ['LC_ALL'] = old_lc_all
    else:
        del os.environ['LC_ALL']
    assert translation.call_count == 1
    assert translation.call_args[1]['languages'] == ['en']
