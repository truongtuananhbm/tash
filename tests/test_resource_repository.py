"""Test resource_repository
"""
from typing import List

from sqlalchemy import text
import operator
from sqlalchemy.sql.elements import BinaryExpression, literal
import pytest
from copy import copy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import BinaryExpression
from app.src.models import Resource
from app.src.repositories.resource import FileRepository
from app.src.schemas.resource import ResourceGet
def test_search_resources(mocker, session_mock, sample_resources):
    """Test search_resources method."""
    resource_repository = FileRepository(Resource)
    query_mock = mocker.patch.object(session_mock, 'query')
    query_mock.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.all.return_value = sample_resources
    filter = ResourceGet(
        id=1,
        stage_id=1,
        status_id=1,
        name="TTA1",
        version=1,
        platform_id=1,
        product_type_id=1,
        repo_id=1,
        tag_id=1,
    )
    result = resource_repository.search_resources(session_mock, filter)
    assert result == sample_resources
    assert isinstance(result, list)
def test_search_resources_error(session_mock, mocker):
    """Test exception search_resources method.
    """
    resource_repository = FileRepository(Resource)

    query_mock = mocker.patch.object(session_mock, 'query')
    query_mock.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.filter.return_value.all.side_effect = SQLAlchemyError
    filter = ResourceGet(
        id=1,
        stage_id=1,
        status_id=1,
        name="TTA1",
        version=1,
        platform_id=1,
        product_type_id=1,
        repo_id=1,
        tag_id=1,
    )
    with pytest.raises(Exception) as e:
        resource_repository.search_resources(session_mock, filter)
        assert e.message == "Database Error"














