"""Compiler variables."""

import enum
import os
from enum import Enum
from types import SimpleNamespace

from reflex.base import Base
from reflex.constants import ENV_MODE_ENV_VAR, Dirs, Env
from reflex.utils.imports import ImportVar

# The prefix used to create setters for state vars.
SETTER_PREFIX = "set_"

# The file used to specify no compilation.
NOCOMPILE_FILE = "nocompile"

# The env var to toggle minification of states.
ENV_MINIFY_STATES = "REFLEX_MINIFY_STATES"


class Ext(SimpleNamespace):
    """Extension used in Reflex."""

    # The extension for JS files.
    JS = ".js"
    # The extension for python files.
    PY = ".py"
    # The extension for css files.
    CSS = ".css"
    # The extension for zip files.
    ZIP = ".zip"
    # The extension for executable files on Windows.
    EXE = ".exe"


def minify_states() -> bool:
    """Whether to minify states.

    Returns:
        True if states should be minified.
    """
    env = os.environ.get(ENV_MINIFY_STATES, None)
    if env is not None:
        return env.lower() == "true"

    # minify states in prod by default
    return os.environ.get(ENV_MODE_ENV_VAR, "") == Env.PROD.value


class CompileVars(SimpleNamespace):
    """The variables used during compilation."""

    # The expected variable name where the rx.App is stored.
    APP = "app"
    # The expected variable name where the API object is stored for deployment.
    API = "api"
    # The name of the router variable.
    ROUTER = "router"
    # The name of the socket variable.
    SOCKET = "socket"
    # The name of the variable to hold API results.
    RESULT = "result"
    # The name of the final variable.
    FINAL = "final"
    # The name of the process variable.
    PROCESSING = "processing"
    # The name of the state variable.
    STATE = "state"
    # The name of the events variable.
    EVENTS = "events"
    # The name of the initial hydrate event.
    HYDRATE = "hydrate"
    # The name of the is_hydrated variable.
    IS_HYDRATED = "is_hydrated"
    # The name of the function to add events to the queue.
    ADD_EVENTS = "addEvents"
    # The name of the var storing any connection error.
    CONNECT_ERROR = "connectErrors"
    # The name of the function for converting a dict to an event.
    TO_EVENT = "Event"

    # Whether to minify states.
    MINIFY_STATES = minify_states()

    # The name of the OnLoadInternal state.
    ON_LOAD_INTERNAL_STATE = (
        "l" if MINIFY_STATES else "reflex___state____on_load_internal_state"
    )
    # The name of the internal on_load event.
    ON_LOAD_INTERNAL = f"{ON_LOAD_INTERNAL_STATE}.on_load_internal"
    # The name of the UpdateVarsInternal state.
    UPDATE_VARS_INTERNAL_STATE = (
        "u" if MINIFY_STATES else "reflex___state____update_vars_internal_state"
    )
    # The name of the internal event to update generic state vars.
    UPDATE_VARS_INTERNAL = f"{UPDATE_VARS_INTERNAL_STATE}.update_vars_internal"
    # The name of the frontend event exception state
    FRONTEND_EXCEPTION_STATE = (
        "e" if MINIFY_STATES else "reflex___state____frontend_event_exception_state"
    )
    # The full name of the frontend exception state
    FRONTEND_EXCEPTION_STATE_FULL = (
        f"reflex___state____state.{FRONTEND_EXCEPTION_STATE}"
    )
    INTERNAL_STATE_NAMES = {
        ON_LOAD_INTERNAL_STATE,
        UPDATE_VARS_INTERNAL_STATE,
        FRONTEND_EXCEPTION_STATE,
    }


class PageNames(SimpleNamespace):
    """The name of basic pages deployed in NextJS."""

    # The name of the index page.
    INDEX_ROUTE = "index"
    # The name of the app root page.
    APP_ROOT = "_app"
    # The root stylesheet filename.
    STYLESHEET_ROOT = "styles"
    # The name of the document root page.
    DOCUMENT_ROOT = "_document"
    # The name of the theme page.
    THEME = "theme"
    # The module containing components.
    COMPONENTS = "components"
    # The module containing shared stateful components
    STATEFUL_COMPONENTS = "stateful_components"


class ComponentName(Enum):
    """Component names."""

    BACKEND = "Backend"
    FRONTEND = "Frontend"

    def zip(self):
        """Give the zip filename for the component.

        Returns:
            The lower-case filename with zip extension.
        """
        return self.value.lower() + Ext.ZIP


class Imports(SimpleNamespace):
    """Common sets of import vars."""

    EVENTS = {
        "react": [ImportVar(tag="useContext")],
        f"$/{Dirs.CONTEXTS_PATH}": [ImportVar(tag="EventLoopContext")],
        f"$/{Dirs.STATE_PATH}": [ImportVar(tag=CompileVars.TO_EVENT)],
    }


class Hooks(SimpleNamespace):
    """Common sets of hook declarations."""

    EVENTS = f"const [{CompileVars.ADD_EVENTS}, {CompileVars.CONNECT_ERROR}] = useContext(EventLoopContext);"
    AUTOFOCUS = """
                // Set focus to the specified element.
                const focusRef = useRef(null)
                useEffect(() => {
                  if (focusRef.current) {
                    focusRef.current.focus();
                  }
                })"""


class MemoizationDisposition(enum.Enum):
    """The conditions under which a component should be memoized."""

    # If the component uses state or events, it should be memoized.
    STATEFUL = "stateful"
    ALWAYS = "always"
    NEVER = "never"


class MemoizationMode(Base):
    """The mode for memoizing a Component."""

    # The conditions under which the component should be memoized.
    disposition: MemoizationDisposition = MemoizationDisposition.STATEFUL

    # Whether children of this component should be memoized first.
    recursive: bool = True


class SpecialAttributes(enum.Enum):
    """Special attributes for components.

    These are placed in custom_attrs and rendered as-is rather than converting
    to a style prop.
    """

    DATA_UNDERSCORE = "data_"
    DATA_DASH = "data-"
    ARIA_UNDERSCORE = "aria_"
    ARIA_DASH = "aria-"

    @classmethod
    def is_special(cls, attr: str) -> bool:
        """Check if the attribute is special.

        Args:
            attr: the attribute to check

        Returns:
            True if the attribute is special.
        """
        return any(attr.startswith(value.value) for value in cls)
