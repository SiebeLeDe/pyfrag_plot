from typing import Optional


class PyFragInputError(ValueError):
    def __init__(self, message, key: Optional[str] = None):
        if key is not None:
            message = f"{key} is not valid. {message}"
        super().__init__(message)
        self.key = key


class PyFragResultsProcessingError(ValueError):
    def __init__(self, message, section: str):
        if section is not None:
            message = f"Error in {section}. {message}"
        super().__init__(message)
        self.key = section


class PyFragConfigError(ValueError):
    def __init__(self, section: str):
        message = f"Error in {section}. Pyfrag_plotter is not initialized. Please call initialize_pyfrag_plotter() first."
        super().__init__(message)
        self.key = section


class PyFragResultsObjectError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
