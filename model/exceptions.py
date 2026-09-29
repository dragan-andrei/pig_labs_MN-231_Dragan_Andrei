"""Domain exception hierarchy for computer modeling and catalog operations."""

from __future__ import annotations


class DomainError(Exception):
    """Base domain exception for the laboratory application."""


class EntityValidationError(DomainError):
    """Raised when device parameter validation fails."""


class SortStrategyError(DomainError):
    """Raised when sorting strategy fails or encounters invalid keys."""


class ModelError(DomainError):
    """Raised when model state operation fails."""
