from typing import Optional


# ====================================================================================================
# PyFrag Warning =====================================================================================
# ====================================================================================================

class PyFragResultsProcessingWarning(Warning):
    """An error that occurs when processing PyFrag results."""

    def __init__(self, message, section: str):
        if section is not None:
            message = f"Error in {section}. {message}"
        super().__init__(message)
        self.key = section

# ====================================================================================================
# PyFrag Errors ======================================================================================
# ====================================================================================================


class PyFragInputError(ValueError):
    """An error that occurs when the PyFrag input is invalid."""

    def __init__(self, message, key: Optional[str] = None):
        if key is not None:
            message = f"{key} is not valid. {message}"
        super().__init__(message)
        self.key = key


class PyFragResultsProcessingError(ValueError):
    """An error that occurs when processing PyFrag results."""

    def __init__(self, message, section: str):
        if section is not None:
            message = f"Error in {section}. {message}"
        super().__init__(message)
        self.key = section


class PyFragConfigError(ValueError):
    """An error that occurs when the PyFrag configuration is invalid."""

    def __init__(self, section: str):
        message = f"Error in {section}. Pyfrag_plotter is not initialized. Please call initialize_pyfrag_plotter() first."
        super().__init__(message)
        self.key = section


class PyFragResultsObjectError(ValueError):
    """An error that occurs when a PyFrag results object is invalid."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
