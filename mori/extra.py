# https://github.com/naryal2580/dore/blob/e753f8ac1bc6119ca9da066d48f90c171d135453/dore/core.py#L129
def match(method='regex', object1=None, object2=None):
    """
    Tries to check if content of object1 == object2
    methods = ('regex', 'length', 'headers', 'json', 'resp_code')

        Returns:
            bool: Boolean if, content of those objects match

        Parametes:
            method (str): Method for the match to work with
        
                if method is 'regex:
                    NOTE: Content of both objects are automatically converted into bytes-like object
                    object1: Response content / Response object for comparision
                    object2: Regex pattern for the comparision
        
                if method is 'length':
                    NOTE: Content of both objects are automatically converted into bytes-like object
                    object1: Object whoose length needs to be compared with
                    object2: Length, or any object with length
                
                if method is 'headers':
                    NOTE: Content of object1 is automatically converted into case insensative `dict` object
                    object1: Object whoose HTTP headers needs to be compared
                    object2 (dict/list): Dictionary of headers to match from the response (uses regex on values)

                        if type(object2) is list or tuple:
                            # **ONLY** checks if the list of passed headers are present (keys check)
                
                if method is 'json':
                    NOTE: Content of object1 is automatically converted into case insensative `dict` object
                    object1: Object whoose JSON response needs to be compared with
                    object2: JSON to compare response json with (uses regex on values)

                        if type(object2) is list or tuple:
                            # Will only check if `keys` are present on the JSON
                
                if method is 'resp_code':
                    NOTE: I just added this, because why not ;)
                    object1: Object containing response code
                    object2: response code to check with object1
    """
    if object1 == object2:
        return True

    if method in ('regex', 're'):
        content, pattern = bytify(object1), bytify(object2)
        if regex.search(pattern, content):  # I now leave everything else to this :p
            return True
        else:
            return False

    elif method in ('headers', 'head', 'header', 'heads'):
        if type(object1) == http_response:
            object1 = object1.headers
        object1 = case_insensative_dict(object1)
        if type(object2) in (list, tuple):
            for key in object2:
                if key not in object1:
                    return False
            return True
        else:
            for key in object2:
                if key in object1:
                    if not match('regex', object1[key], object2[key]):
                        return False
                else:
                    return False
            return True

    elif method == 'json':
        if type(object1) == http_response:
            if object1.headers['Content-Type'] != 'application/json':
                print(warn('WARN -> Response `Content-Type` is not `json`, continuing..'))
            object1 = object1.json()
        elif type(object1) in (str, bytes):
            object1 = json.loads(object1)
        elif isinstance(object, (TextIOBase, BufferedIOBase, RawIOBase, IOBase)):
            object1 = json.load(object1)
        object1 = case_insensative_dict(object1)
        if type(object2) in (list, tuple):
            for key in object2:
                if key not in object1:
                    return False
            return True
        else:
            if type(object2) in (str, bytes):
                object2 = json.loads(object2)
            elif isinstance(object, (TextIOBase, BufferedIOBase, RawIOBase, IOBase)):
                object2 = json.load(object2)
            for key in object2:
                    if key in object1:
                        if not match('regex', object1[key], object2[key]):
                            return False
                    else:
                        return False
            return True

    elif method in ('len', 'length'):
        if type(object2) in (str, bytes):
            if object2.isdigit():
                object2 = b' ' * int(object2)
        elif type(object2) == int:
            object2 = b' ' * object2
        object1, object2 = bytify(object1), bytify(object2)
        cmp1, cmp2 = len(object1), len(object2)

    elif method in ('resp_code', 'status_code', 'response_code'):
        cmp1 = cmp2 = 0
        if type(object1) == http_response:
            object1 = object1.status_code
        cmp1, cmp2 = int(object1), int(object2)
    
    else:
        print(bad('WTH -> UNKNOWN METHOD USED'))


    if cmp1 == cmp2:  # Left comparision from length, response status code
        return True
    else:
        return False


# https://github.com/c4p-n1ck/dore/blob/4ebd9d15039b6064f8c1aaf1f8c6e5ad44bfaccd/dore/extra.py#L125
def bytify(object):
    """
    Converts content of given object into bytes-like object

        Parameters:
            object (...): Almost any object (io object, response object, str, json, list...)

        Returns:
            object (bytes): Result bytes-like object
    """
    if type(object) == None:  # Hard-coded None object, for a reason. 
        return None

    elif type(object) == bytes:
        return object

    elif type(object) == http_response:
        object = object.content  # This is always `bytes` object

    elif isinstance(object, (TextIOBase, BufferedIOBase, RawIOBase, IOBase)):
        try:  
            object = bytify(object.read())
        except:
            # Will not interrupt the flow, but might cause a flaw
            object = bytify(str(object))

    else:
        print(warn('Expected object might not be returned'))
        # WARN: If object type is unknown from above categories, THIS MIGHT BE AN ISSUE!
        object = str(object).encode()

    return object


def chunkify(iterable, chunk_length=4):
    """
    Yield chunk_length-sized chunks from an iterable

        Parameters:
            iterable: An iterable
            chunk_length: Chunk size for the iterable to be splitted

        Retuns:
            iterable: Chunked iterable

    Copied from: https://stackoverflow.com/a/312464/190597
    """
    for _ in range(0, len(iterable), chunk_length):
        yield iterable[_:_ + chunk_length]
