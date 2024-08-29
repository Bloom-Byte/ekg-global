
class CriteriaException(Exception):
    pass


class ValidationError(CriteriaException):
    pass


class FunctionSpecValidationError(ValidationError):
    pass


class UnsupportedFunction(FunctionSpecValidationError):
    pass


class CriterionValidationError(ValidationError):
    pass


class ComparisonExecutorNotFound(CriteriaException):
    pass
