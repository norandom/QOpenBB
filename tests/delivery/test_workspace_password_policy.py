"""Execute real schema definitions without importing database/service startup."""
import ast
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Annotated

import pytest
from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field, ValidationError

SOURCE = Path(__file__).resolve().parents[2] / 'vendor/workspace/backend-api/backend/api/schemas.py'


@pytest.fixture
def schemas():
    names = {'check_password', 'ExternalUserLogin', 'UserLogin', 'ProUserLogin',
             'OAuthLogin', 'UserUpdate', 'UserCreate', 'UserReset'}
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    selected = [node for node in tree.body if getattr(node, 'name', None) in names]
    regex = next(node for node in tree.body if isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id == 'VALID_REGEX'
                         for target in node.targets))
    namespace = dict(BaseModel=BaseModel, UserMarketing=BaseModel, Annotated=Annotated,
                     AfterValidator=AfterValidator, BeforeValidator=BeforeValidator,
                     Field=Field, main_config=ConfigDict(extra='forbid'), re=re,
                     EmailStr=str, IPvAnyAddress=str, source_type=str,
                     check_email=lambda value: value, check_username=lambda value: value,
                     check_email_or_username=lambda value: value,
                     check_totp_token=lambda value: value, blank_to_none=lambda value: value,
                     base=SimpleNamespace())
    exec(compile(ast.Module(body=[regex, *selected], type_ignores=[]), str(SOURCE), 'exec'), namespace)
    return SimpleNamespace(**namespace)


@pytest.mark.parametrize('model', ['UserLogin', 'ProUserLogin'])
@pytest.mark.parametrize('password', ['CHANGE_ME', 'x', ' leading space ', ' ', 'é'])
def test_existing_password_is_preserved(schemas, model, password):
    result = getattr(schemas, model)(email='synthetic@example.com', password=password)
    assert result.password == password


@pytest.mark.parametrize('model', ['UserLogin', 'ProUserLogin'])
@pytest.mark.parametrize('payload', [{}, {'password': ''}, {'password': None}])
def test_login_requires_nonempty_password(schemas, model, payload):
    with pytest.raises(ValidationError):
        getattr(schemas, model)(email='synthetic@example.com', **payload)


def test_current_password_reaches_hash_verification_unchanged(schemas):
    calls = []
    schemas.base.verify_password = lambda plain, hashed: calls.append((plain, hashed)) or True
    update = schemas.UserUpdate(old_password=' CHANGE_ME ', new_password='Fresh1!Password')
    assert update.validated_dict('synthetic-hash')['password'] == 'Fresh1!Password'
    assert calls == [(' CHANGE_ME ', 'synthetic-hash')]
    schemas.base.verify_password = lambda plain, hashed: False
    with pytest.raises(ValueError, match='Invalid password'):
        update.validated_dict('synthetic-hash')


def test_current_password_remains_optional_but_cannot_be_empty(schemas):
    assert schemas.UserUpdate().old_password is None
    assert schemas.UserUpdate(old_password=None).old_password is None
    with pytest.raises(ValidationError):
        schemas.UserUpdate(old_password='')


@pytest.mark.parametrize('password', ['CHANGE_ME', 'x', 'Lowercase1', 'Fresh1! Password'])
@pytest.mark.parametrize('model', ['UserCreate', 'UserReset', 'UserUpdate'])
def test_new_passwords_keep_strength_policy(schemas, model, password):
    payload = {'UserCreate': {'email': 'synthetic@example.com', 'password': password},
               'UserReset': {'token': 'synthetic-token', 'password': password},
               'UserUpdate': {'old_password': 'Old1!Password', 'new_password': password}}
    with pytest.raises(ValidationError):
        getattr(schemas, model)(**payload[model])


def test_strong_new_passwords_and_oauth_remain_valid(schemas):
    assert schemas.UserCreate(email='synthetic@example.com', password='Fresh1!Password').password
    assert schemas.UserReset(token='synthetic-token', password='Fresh1!Password').password
    assert schemas.UserUpdate(new_password='Fresh1!Password').new_password
    assert schemas.OAuthLogin(email='synthetic@example.com').password is None
