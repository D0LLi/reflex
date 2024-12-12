"""Stub file for reflex/components/base/error_boundary.py"""

# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------
from typing import Any, Dict, Optional, Tuple, Union, overload

from reflex.components.component import Component
from reflex.event import BASE_STATE, EventType
from reflex.style import Style
from reflex.vars.base import Var

def on_error_spec(
    error: Var[Dict[str, str]], info: Var[Dict[str, str]]
) -> Tuple[Var[str], Var[str]]: ...

class ErrorBoundary(Component):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        fallback_render: Optional[Union[Component, Var[Component]]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, Any]]] = None,
        on_blur: Optional[EventType[[], BASE_STATE]] = None,
        on_click: Optional[EventType[[], BASE_STATE]] = None,
        on_context_menu: Optional[EventType[[], BASE_STATE]] = None,
        on_double_click: Optional[EventType[[], BASE_STATE]] = None,
        on_error: Optional[
            Union[
                EventType[[], BASE_STATE],
                EventType[[str], BASE_STATE],
                EventType[[str, str], BASE_STATE],
            ]
        ] = None,
        on_focus: Optional[EventType[[], BASE_STATE]] = None,
        on_mount: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_down: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_enter: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_leave: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_move: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_out: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_over: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_up: Optional[EventType[[], BASE_STATE]] = None,
        on_scroll: Optional[EventType[[], BASE_STATE]] = None,
        on_unmount: Optional[EventType[[], BASE_STATE]] = None,
        **props,
    ) -> "ErrorBoundary":
        """Create an ErrorBoundary component.

        Args:
            *children: The children of the component.
            on_error: Fired when the boundary catches an error.
            fallback_render: Rendered instead of the children when an error is caught.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the component.

        Returns:
            The ErrorBoundary component.
        """
        ...

error_boundary = ErrorBoundary.create
