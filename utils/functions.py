""" File with many util functions """

def keyHasValue(customObject: object, key: str):
    """
        Checks if the dictionary/object has the key, if not set to None

        Args:
            customObjects {object}: Object to check
            key {str}: Key to be checked
        
        Returns:
            object value or null
    """
    if key in customObject:
        if customObject[key] is not None:
            if customObject[key] != '':
                if key == 'price':
                    return float(customObject[key])
                return customObject[key]

            return None
        return None
    return None


def checkAndReplace(value: str) -> str:
    """
        Checks if the entering value has quotes on it, and removes them

        Args:
            value {str}: Value to be formated
        
        Returns:
            formated value without quotes
    """
    return value.replace('"', '')