class ResponseStatusCodeException(Exception):
    pass


class ResponseErrorException(Exception):
    pass


class ResponseJsonParseError(Exception):
    pass


class MissingAuthorizationCookie(Exception):
    pass
