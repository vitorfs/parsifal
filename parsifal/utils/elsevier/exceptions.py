class ElsevierException(Exception):
    pass

class ElsevierInvalidRequest(ElsevierException):
    '''
    Status Code 400
    '''
    pass

class ElsevierQuotaExceeded(ElsevierException):
    '''
    Status Code 429
    '''
    pass