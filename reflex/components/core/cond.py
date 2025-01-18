"""Create a list of components from an iterable."""

from __future__ import annotations

from typing import Any, overload

from reflex.components.base.fragment import Fragment
from reflex.components.component import BaseComponent, Component
from reflex.style import LIGHT_COLOR_MODE, resolved_color_mode
from reflex.utils.types import infallible_issubclass
from reflex.vars.base import LiteralVar, ReflexCallable, Var
from reflex.vars.function import ArgsFunctionOperation
from reflex.vars.number import ternary_operation


@overload
def cond(condition: Any, c1: Component, c2: Any = None) -> Component: ...


@overload
def cond(condition: Any, c1: Any, c2: Any) -> Var: ...


def cond(condition: Any, c1: Any, c2: Any = None) -> Component | Var:
    """Create a conditional component or Prop.

    Args:
        condition: The cond to determine which component to render.
        c1: The component or prop to render if the cond_var is true.
        c2: The component or prop to render if the cond_var is false.

    Returns:
        The conditional component.

    Raises:
        ValueError: If the arguments are invalid.
    """
    # Convert the condition to a Var.
    cond_var = LiteralVar.create(condition)

    # If the first component is a component, create a Fragment if the second component is not set.
    if isinstance(c1, BaseComponent) or (
        isinstance(c1, Var) and infallible_issubclass(c1._var_type, BaseComponent)
    ):
        c2 = c2 if c2 is not None else Fragment.create()

    # Check that the second argument is valid.
    if c2 is None:
        raise ValueError("For conditional vars, the second argument must be set.")

    c1 = Var.create(c1)
    c2 = Var.create(c2)

    # Create the conditional var.
    return ternary_operation(
        cond_var.bool(),
        ArgsFunctionOperation.create(
            (),
            c1,
            _var_type=ReflexCallable[[], c1._var_type],
        ),
        ArgsFunctionOperation.create(
            (),
            c2,
            _var_type=ReflexCallable[[], c2._var_type],
        ),
    ).call()


@overload
def color_mode_cond(light: Component, dark: Component | None = None) -> Component: ...  # type: ignore


@overload
def color_mode_cond(light: Any, dark: Any = None) -> Var: ...


def color_mode_cond(light: Any, dark: Any = None) -> Var | Component:
    """Create a component or Prop based on color_mode.

    Args:
        light: The component or prop to render if color_mode is default
        dark: The component or prop to render if color_mode is non-default

    Returns:
        The conditional component or prop.
    """
    return cond(
        resolved_color_mode == LiteralVar.create(LIGHT_COLOR_MODE),
        light,
        dark,
    )
