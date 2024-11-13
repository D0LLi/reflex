"""Immutable function vars."""

from __future__ import annotations

import dataclasses
import sys
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union, overload

from typing_extensions import Concatenate, Generic, ParamSpec, Protocol, TypeVar

from reflex.utils import format
from reflex.utils.exceptions import VarTypeError
from reflex.utils.types import GenericType

from .base import CachedVarOperation, LiteralVar, Var, VarData, cached_property_no_lock

P = ParamSpec("P")
V1 = TypeVar("V1")
V2 = TypeVar("V2")
V3 = TypeVar("V3")
V4 = TypeVar("V4")
V5 = TypeVar("V5")
V6 = TypeVar("V6")
R = TypeVar("R")


class ReflexCallable(Protocol[P, R]):
    """Protocol for a callable."""

    __call__: Callable[P, R]


CALLABLE_TYPE = TypeVar("CALLABLE_TYPE", bound=ReflexCallable, infer_variance=True)
OTHER_CALLABLE_TYPE = TypeVar(
    "OTHER_CALLABLE_TYPE", bound=ReflexCallable, infer_variance=True
)


class FunctionVar(Var[CALLABLE_TYPE], default_type=ReflexCallable[Any, Any]):
    """Base class for immutable function vars."""

    @overload
    def partial(self) -> FunctionVar[CALLABLE_TYPE]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[Concatenate[V1, P], R]],
        arg1: Union[V1, Var[V1]],
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[Concatenate[V1, V2, P], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[Concatenate[V1, V2, V3, P], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[Concatenate[V1, V2, V3, V4, P], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
        arg4: Union[V4, Var[V4]],
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[Concatenate[V1, V2, V3, V4, V5, P], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
        arg4: Union[V4, Var[V4]],
        arg5: Union[V5, Var[V5]],
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[Concatenate[V1, V2, V3, V4, V5, V6, P], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
        arg4: Union[V4, Var[V4]],
        arg5: Union[V5, Var[V5]],
        arg6: Union[V6, Var[V6]],
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(
        self: FunctionVar[ReflexCallable[P, R]], *args: Var | Any
    ) -> FunctionVar[ReflexCallable[P, R]]: ...

    @overload
    def partial(self, *args: Var | Any) -> FunctionVar: ...

    def partial(self, *args: Var | Any) -> FunctionVar:  # type: ignore
        """Partially apply the function with the given arguments.

        Args:
            *args: The arguments to partially apply the function with.

        Returns:
            The partially applied function.
        """
        if not args:
            return self
        remaining_validators = self._pre_check(*args)
        if self.__call__ is self.partial:
            # if the default behavior is partial, we should return a new partial function
            return ArgsFunctionOperationBuilder.create(
                (),
                VarOperationCall.create(self, *args, Var(_js_expr="...args")),
                rest="args",
                validators=remaining_validators,
            )
        return ArgsFunctionOperation.create(
            (),
            VarOperationCall.create(self, *args, Var(_js_expr="...args")),
            rest="args",
            validators=remaining_validators,
        )

    @overload
    def call(
        self: FunctionVar[ReflexCallable[[V1], R]], arg1: Union[V1, Var[V1]]
    ) -> VarOperationCall[[V1], R]: ...

    @overload
    def call(
        self: FunctionVar[ReflexCallable[[V1, V2], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
    ) -> VarOperationCall[[V1, V2], R]: ...

    @overload
    def call(
        self: FunctionVar[ReflexCallable[[V1, V2, V3], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
    ) -> VarOperationCall[[V1, V2, V3], R]: ...

    @overload
    def call(
        self: FunctionVar[ReflexCallable[[V1, V2, V3, V4], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
        arg4: Union[V4, Var[V4]],
    ) -> VarOperationCall[[V1, V2, V3, V4], R]: ...

    @overload
    def call(
        self: FunctionVar[ReflexCallable[[V1, V2, V3, V4, V5], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
        arg4: Union[V4, Var[V4]],
        arg5: Union[V5, Var[V5]],
    ) -> VarOperationCall[[V1, V2, V3, V4, V5], R]: ...

    @overload
    def call(
        self: FunctionVar[ReflexCallable[[V1, V2, V3, V4, V5, V6], R]],
        arg1: Union[V1, Var[V1]],
        arg2: Union[V2, Var[V2]],
        arg3: Union[V3, Var[V3]],
        arg4: Union[V4, Var[V4]],
        arg5: Union[V5, Var[V5]],
        arg6: Union[V6, Var[V6]],
    ) -> VarOperationCall[[V1, V2, V3, V4, V5, V6], R]: ...

    @overload
    def call(
        self: FunctionVar[ReflexCallable[P, R]], *args: Var | Any
    ) -> VarOperationCall[P, R]: ...

    @overload
    def call(self, *args: Var | Any) -> Var: ...

    def call(self, *args: Var | Any) -> Var:  # type: ignore
        """Call the function with the given arguments.

        Args:
            *args: The arguments to call the function with.

        Returns:
            The function call operation.
        """
        self._pre_check(*args)
        return VarOperationCall.create(self, *args).guess_type()

    def _pre_check(self, *args: Var | Any) -> Tuple[Callable[[Any], bool], ...]:
        """Check if the function can be called with the given arguments.

        Args:
            *args: The arguments to call the function with.

        Returns:
            True if the function can be called with the given arguments.
        """
        return tuple()

    __call__ = call


class BuilderFunctionVar(
    FunctionVar[CALLABLE_TYPE], default_type=ReflexCallable[Any, Any]
):
    """Base class for immutable function vars with the builder pattern."""

    __call__ = FunctionVar.partial


class FunctionStringVar(FunctionVar[CALLABLE_TYPE]):
    """Base class for immutable function vars from a string."""

    @classmethod
    def create(
        cls,
        func: str,
        _var_type: Type[OTHER_CALLABLE_TYPE] = ReflexCallable[Any, Any],
        _var_data: VarData | None = None,
    ) -> FunctionStringVar[OTHER_CALLABLE_TYPE]:
        """Create a new function var from a string.

        Args:
            func: The function to call.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The function var.
        """
        return FunctionStringVar(
            _js_expr=func,
            _var_type=_var_type,
            _var_data=_var_data,
        )


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class VarOperationCall(Generic[P, R], CachedVarOperation, Var[R]):
    """Base class for immutable vars that are the result of a function call."""

    _func: Optional[FunctionVar[ReflexCallable[P, R]]] = dataclasses.field(default=None)
    _args: Tuple[Union[Var, Any], ...] = dataclasses.field(default_factory=tuple)

    @cached_property_no_lock
    def _cached_var_name(self) -> str:
        """The name of the var.

        Returns:
            The name of the var.
        """
        return f"({str(self._func)}({', '.join([str(LiteralVar.create(arg)) for arg in self._args])}))"

    @cached_property_no_lock
    def _cached_get_all_var_data(self) -> VarData | None:
        """Get all the var data associated with the var.

        Returns:
            All the var data associated with the var.
        """
        return VarData.merge(
            self._func._get_all_var_data() if self._func is not None else None,
            *[LiteralVar.create(arg)._get_all_var_data() for arg in self._args],
            self._var_data,
        )

    @classmethod
    def create(
        cls,
        func: FunctionVar[ReflexCallable[P, R]],
        *args: Var | Any,
        _var_type: GenericType = Any,
        _var_data: VarData | None = None,
    ) -> VarOperationCall:
        """Create a new function call var.

        Args:
            func: The function to call.
            *args: The arguments to call the function with.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The function call var.
        """
        function_return_type = (
            func._var_type.__args__[1]
            if getattr(func._var_type, "__args__", None)
            else Any
        )
        var_type = _var_type if _var_type is not Any else function_return_type
        return cls(
            _js_expr="",
            _var_type=var_type,
            _var_data=_var_data,
            _func=func,
            _args=args,
        )


@dataclasses.dataclass(frozen=True)
class DestructuredArg:
    """Class for destructured arguments."""

    fields: Tuple[str, ...] = tuple()
    rest: Optional[str] = None

    def to_javascript(self) -> str:
        """Convert the destructured argument to JavaScript.

        Returns:
            The destructured argument in JavaScript.
        """
        return format.wrap(
            ", ".join(self.fields) + (f", ...{self.rest}" if self.rest else ""),
            "{",
            "}",
        )


@dataclasses.dataclass(
    frozen=True,
)
class FunctionArgs:
    """Class for function arguments."""

    args: Tuple[Union[str, DestructuredArg], ...] = tuple()
    rest: Optional[str] = None


def format_args_function_operation(
    args: FunctionArgs, return_expr: Var | Any, explicit_return: bool
) -> str:
    """Format an args function operation.

    Args:
        args: The function arguments.
        return_expr: The return expression.
        explicit_return: Whether to use explicit return syntax.

    Returns:
        The formatted args function operation.
    """
    arg_names_str = ", ".join(
        [arg if isinstance(arg, str) else arg.to_javascript() for arg in args.args]
        + ([f"...{args.rest}"] if args.rest else [])
    )

    return_expr_str = str(LiteralVar.create(return_expr))

    # Wrap return expression in curly braces if explicit return syntax is used.
    return_expr_str_wrapped = (
        format.wrap(return_expr_str, "{", "}") if explicit_return else return_expr_str
    )

    return f"(({arg_names_str}) => {return_expr_str_wrapped})"


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class ArgsFunctionOperation(CachedVarOperation, FunctionVar):
    """Base class for immutable function defined via arguments and return expression."""

    _args: FunctionArgs = dataclasses.field(default_factory=FunctionArgs)
    _validators: Tuple[Callable[[Any], bool], ...] = dataclasses.field(
        default_factory=tuple
    )
    _return_expr: Union[Var, Any] = dataclasses.field(default=None)
    _function_name: str = dataclasses.field(default="")
    _explicit_return: bool = dataclasses.field(default=False)

    @cached_property_no_lock
    def _cached_var_name(self) -> str:
        """The name of the var.

        Returns:
            The name of the var.
        """
        return format_args_function_operation(
            self._args, self._return_expr, self._explicit_return
        )

    def _pre_check(self, *args: Var | Any) -> Tuple[Callable[[Any], bool], ...]:
        """Check if the function can be called with the given arguments.

        Args:
            *args: The arguments to call the function with.

        Returns:
            True if the function can be called with the given arguments.
        """
        for i, (validator, arg) in enumerate(zip(self._validators, args)):
            if not validator(arg):
                arg_name = self._args.args[i] if i < len(self._args.args) else None
                if arg_name is not None:
                    raise VarTypeError(
                        f"Invalid argument {str(arg)} provided to {arg_name} in {self._function_name or 'var operation'}"
                    )
                raise VarTypeError(
                    f"Invalid argument {str(arg)} provided to argument {i} in {self._function_name or 'var operation'}"
                )
        return self._validators[len(args) :]

    @classmethod
    def create(
        cls,
        args_names: Sequence[Union[str, DestructuredArg]],
        return_expr: Var | Any,
        rest: str | None = None,
        validators: Sequence[Callable[[Any], bool]] = (),
        function_name: str = "",
        explicit_return: bool = False,
        _var_type: GenericType = Callable,
        _var_data: VarData | None = None,
    ):
        """Create a new function var.

        Args:
            args_names: The names of the arguments.
            return_expr: The return expression of the function.
            rest: The name of the rest argument.
            validators: The validators for the arguments.
            function_name: The name of the function.
            explicit_return: Whether to use explicit return syntax.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The function var.
        """
        return cls(
            _js_expr="",
            _var_type=_var_type,
            _var_data=_var_data,
            _args=FunctionArgs(args=tuple(args_names), rest=rest),
            _function_name=function_name,
            _validators=tuple(validators),
            _return_expr=return_expr,
            _explicit_return=explicit_return,
        )


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class ArgsFunctionOperationBuilder(CachedVarOperation, BuilderFunctionVar):
    """Base class for immutable function defined via arguments and return expression with the builder pattern."""

    _args: FunctionArgs = dataclasses.field(default_factory=FunctionArgs)
    _validators: Tuple[Callable[[Any], bool], ...] = dataclasses.field(
        default_factory=tuple
    )
    _return_expr: Union[Var, Any] = dataclasses.field(default=None)
    _function_name: str = dataclasses.field(default="")
    _explicit_return: bool = dataclasses.field(default=False)

    @cached_property_no_lock
    def _cached_var_name(self) -> str:
        """The name of the var.

        Returns:
            The name of the var.
        """
        return format_args_function_operation(
            self._args, self._return_expr, self._explicit_return
        )

    def _pre_check(self, *args: Var | Any) -> Tuple[Callable[[Any], bool], ...]:
        """Check if the function can be called with the given arguments.

        Args:
            *args: The arguments to call the function with.

        Returns:
            True if the function can be called with the given arguments.
        """
        for i, (validator, arg) in enumerate(zip(self._validators, args)):
            if not validator(arg):
                arg_name = self._args.args[i] if i < len(self._args.args) else None
                if arg_name is not None:
                    raise VarTypeError(
                        f"Invalid argument {str(arg)} provided to {arg_name} in {self._function_name or 'var operation'}"
                    )
                raise VarTypeError(
                    f"Invalid argument {str(arg)} provided to argument {i} in {self._function_name or 'var operation'}"
                )
        return self._validators[len(args) :]

    @classmethod
    def create(
        cls,
        args_names: Sequence[Union[str, DestructuredArg]],
        return_expr: Var | Any,
        rest: str | None = None,
        validators: Sequence[Callable[[Any], bool]] = (),
        function_name: str = "",
        explicit_return: bool = False,
        _var_type: GenericType = Callable,
        _var_data: VarData | None = None,
    ):
        """Create a new function var.

        Args:
            args_names: The names of the arguments.
            return_expr: The return expression of the function.
            rest: The name of the rest argument.
            validators: The validators for the arguments.
            function_name: The name of the function.
            explicit_return: Whether to use explicit return syntax.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The function var.
        """
        return cls(
            _js_expr="",
            _var_type=_var_type,
            _var_data=_var_data,
            _args=FunctionArgs(args=tuple(args_names), rest=rest),
            _function_name=function_name,
            _validators=tuple(validators),
            _return_expr=return_expr,
            _explicit_return=explicit_return,
        )


if python_version := sys.version_info[:2] >= (3, 10):
    JSON_STRINGIFY = FunctionStringVar.create(
        "JSON.stringify", _var_type=ReflexCallable[[Any], str]
    )
    ARRAY_ISARRAY = FunctionStringVar.create(
        "Array.isArray", _var_type=ReflexCallable[[Any], bool]
    )
    PROTOTYPE_TO_STRING = FunctionStringVar.create(
        "((__to_string) => __to_string.toString())",
        _var_type=ReflexCallable[[Any], str],
    )
else:
    JSON_STRINGIFY = FunctionStringVar.create(
        "JSON.stringify", _var_type=ReflexCallable[Any, str]
    )
    ARRAY_ISARRAY = FunctionStringVar.create(
        "Array.isArray", _var_type=ReflexCallable[Any, bool]
    )
    PROTOTYPE_TO_STRING = FunctionStringVar.create(
        "((__to_string) => __to_string.toString())",
        _var_type=ReflexCallable[Any, str],
    )
