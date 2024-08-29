
class CriteriaException(Exception):
    pass


class ValidationError(CriteriaException):
    pass


class FunctionValidationError(ValidationError):
    pass


class UnsupportedFunction(FunctionValidationError):
    pass


class CriterionValidationError(ValidationError):
    pass


class ComparisonExecutorNotFound(CriteriaException):
    pass
