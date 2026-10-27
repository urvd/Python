from calculateur.core.commun.erreur.commun_exception import CommunException
from calculateur.core.commun.erreur.error_type import ErrorType


def test_reconnait_number_format_exception():
    exception = CommunException(ErrorType.NUMBER_FORMAT_ERROR, ValueError("nombre invalide"))
    assert exception.error_type == ErrorType.NUMBER_FORMAT_ERROR


def test_reconnait_arithmetic_exception():
    exception = CommunException(ErrorType.ARITHMETIC_ERROR, ZeroDivisionError("division par zéro"))
    assert exception.error_type == ErrorType.ARITHMETIC_ERROR


def test_reconnait_array_index_out_of_bounds_exception():
    exception = CommunException(ErrorType.ARRAY_INDEX_OUT_OF_BOUNDS_ERROR, IndexError(5))
    assert exception.error_type == ErrorType.ARRAY_INDEX_OUT_OF_BOUNDS_ERROR


def test_reconnait_illegal_argument_exception():
    exception = CommunException(ErrorType.ILLEGAL_ARGUMENT_ERROR, ValueError("argument invalide"))
    assert exception.error_type == ErrorType.ILLEGAL_ARGUMENT_ERROR


def test_reconnait_autre_uncatched_exception():
    exception = CommunException(ErrorType.UNDEFINED_ERROR, Exception("argument invalide"))
    assert exception.error_type == ErrorType.UNDEFINED_ERROR
