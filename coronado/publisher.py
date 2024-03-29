# vim: set fileencoding=utf-8:


from coronado import CoronadoAPIError
from coronado import CoronadoMalformedObjectError
from coronado import CoronadoUnprocessableObjectError
from coronado import TripleObject
from coronado.baseobjects import BASE_PUBLISHER_DICT

import json

import requests


# +++ constants +++

_SERVICE_PATH = 'partner/publishers'


# *** classes and objects ***

class Publisher(TripleObject):
    def __init__(self, obj = BASE_PUBLISHER_DICT):
        TripleObject.__init__(self, obj)

        requiredAttributes = [ 'objID', 'assumedName', 'address', 'createdAt', 'updatedAt', ]

        self.assertAll(requiredAttributes)


    @classmethod
    def create(klass, pubSpec : dict) -> object:
        """
        Create a new Publisher instance using the pubSpec.

        Arguments
        ---------
        pubSpec : dict
            A snake_case publisher input as expected by the triple API
            operation:  https://api.partners.dev.tripleupdev.com/docs#operation/createPublisher

        Returns
        -------
            A new Publisher instance

        Raises
        ------
        CoronadoUnprocessableObjectError
            When the payload syntax is correct but the semantics are invalid
        CoronadoAPIError
            When the service endpoint has an error (500 series)
        CoronadoMalformedObjectError
            When the payload syntax and/or semantics are incorrect, or otherwise the method fails
        """
        if not pubSpec:
            raise CoronadoMalformedObjectError

        endpoint = '/'.join([Publisher.serviceURL, _SERVICE_PATH]) # URL fix later
        headers = { 'Authorization': ' '.join([ Publisher.auth.tokenType, Publisher.auth.token, ]) }
        response = requests.request('POST', endpoint, headers = headers, json = pubSpec)
        
        if response.status_code == 422:
            raise CoronadoUnprocessableObjectError(response.text)
            
        if response.status_code >= 500:
            raise CoronadoAPIError(response.text)

        if response.status_code != 200:
            raise CoronadoMalformedObjectError(response.text)

        return None


    @classmethod
    def list(klass : object) -> list:
        """
        Return a list of publishers.

        Returns
        -------
        A list of Publisher objects
        """
        endpoint = '/'.join([Publisher.serviceURL, _SERVICE_PATH]) # URL fix later
        headers = { 'Authorization': ' '.join([ Publisher.auth.tokenType, Publisher.auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        result = [ TripleObject(obj) for obj in json.loads(response.content)['publishers'] ]

        return result


    @classmethod
    def byID(klass, pubID : str) -> object:
        """
        Return the publisher associated with pubID.

        Arguments
        ---------
        pubID : str
            The account ID associated with the resource to fetch

        Returns
        -------
            The Publisher object associated with pubID or None
        """
        endpoint = '/'.join([Publisher.serviceURL, '%s/%s' % (_SERVICE_PATH, pubID)]) # URL fix later
        # TODO:  Refactor this in a separate private class method:
        headers = { 'Authorization': ' '.join([ Publisher.auth.tokenType, Publisher.auth.token, ]) }
        response = requests.request('GET', endpoint, headers = headers)
        # result = [ TripleObject(obj) for obj in json.loads(response.content)['publishers'] ]

        if response.status_code == 404:
            result = None
        else:
            # TODO:  no data there, can't test yet
            pass

        return result


    @classmethod
    def updateWith(klass, pubID : str, payload : dict) -> object:
        """
        Update the receiver with a new assumed name or update its address.

        Arguments
        ---------
        pubID : str
            The Publisher ID to update
        payload : dict
            A dict object with the appropriate object references:
            - assumed_name
            - address
            The address should be generated using a Coronado Address object and
            then calling its asSnakeCaseDictionary() method

        Returns
        -------
            An updated instance of the Publisher associated with pubID, or None
            if the pubID isn't associated with an existing resource.
        """
        endpoint = '/'.join([Publisher.serviceURL, '%s/%s' % (_SERVICE_PATH, pubID)]) # URL fix later
        # TODO:  Refactor this in a separate private class method:
        headers = { 'Authorization': ' '.join([ Publisher.auth.tokenType, Publisher.auth.token, ]) }
        response = requests.request('PATCH', endpoint, headers = headers, json = payload)
        # result = [ TripleObject(obj) for obj in json.loads(response.content)['publishers'] ]

        if response.status_code == 404:
            result = None
        else:
            raise CoronadoAPIError(response.text)

        return result

