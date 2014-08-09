# -*- coding: utf-8 -*-
"""
    line.client
    ~~~~~~~~~~~

    LineClient for sending and receiving message from LINE server.

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
import rsa
import requests
try:
    import simplejson as json
except ImportError:
    import json

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#from curve import CurveThrift
from curve import CurveThrift
from curve.ttypes import TalkException
from curve.ttypes import ToType, ContentType

class LineAPI(object):
    """This class is a wrapper of LINE API

    """
    LINE_DOMAIN = "http://gd2.line.naver.jp"

    LINE_HTTP_URL          = LINE_DOMAIN + "/api/v4/TalkService.do"
    LINE_HTTP_IN_URL       = LINE_DOMAIN + "/P4"
    LINE_CERTIFICATE_URL   = LINE_DOMAIN + "/Q"
    LINE_SESSION_LINE_URL  = LINE_DOMAIN + "/authct/v1/keys/line"
    LINE_SESSION_NAVER_URL = LINE_DOMAIN + "/authct/v1/keys/naver"

    ip          = "127.0.0.1"
    version     = "3.7.0"
    com_name    = ""
    revision    = 0

    _session = requests.session()
    _headers = {}

    def ready(self):
        """
        After login, make `client` and `client_in` instance
        to communicate with LINE server
        """
        raise Exception("Code is removed because of the request of LINE corporation")

    def tokenLogin(self):
        self.transport = THttpClient.THttpClient(self.LINE_HTTP_URL)
        self.transport.setCustomHeaders(self._headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client   = CurveThrift.Client(self.protocol)
        
    def login(self):
        """Login to LINE server."""
        if self.provider == CurveThrift.Provider.LINE: # LINE
            j = self._get_json(self.LINE_SESSION_LINE_URL)
        else: # NAVER
            j = self._get_json(self.LINE_SESSION_NAVER_URL)

        session_key = j['session_key']
        message     = (chr(len(session_key)) + session_key +
                       chr(len(self.id)) + self.id +
                       chr(len(self.password)) + self.password).encode('utf-8')

        keyname, n, e = j['rsa_key'].split(",")
        pub_key       = rsa.PublicKey(int(n,16), int(e,16))
        crypto        = rsa.encrypt(message, pub_key).encode('hex')

        self.transport = THttpClient.THttpClient(self.LINE_HTTP_URL)
        self.transport.setCustomHeaders(self._headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client   = CurveThrift.Client(self.protocol)

        msg = self._client.loginWithIdentityCredentialForCertificate(
                self.id, self.password, keyname, crypto, False, self.ip,
                self.com_name, self.provider, "")

        self._headers['X-Line-Access'] = msg.verifier
        self._pinCode = msg.pinCode

        print "Enter PinCode '%s' to your mobile phone in 2 minutes"\
                % self._pinCode

        raise Exception("Code is removed because of the request of LINE corporation")

    def _getProfile(self):
        """Get profile information

        :returns: Profile object
                    - picturePath
                    - displayName
                    - phone (base64 encoded?)
                    - allowSearchByUserid
                    - pictureStatus
                    - userid
                    - mid # used for unique id for account
                    - phoneticName
                    - regionCode
                    - allowSearchByEmail
                    - email
                    - statusMessage
        """
        return self._client.getProfile()

    def _getAllContactIds(self):
        """Get all contacts of your LINE account"""
        return self._client.getAllContactIds()

    def _getBlockedContactIds(self):
        """Get all blocked contacts of your LINE account"""
        return self._client.getBlockedContactIds()

    def _getContacts(self, ids):
        """Get contact information list from ids

        :returns: List of Contact list
                    - status
                    - capableVideoCall
                    - dispalyName
                    - settings
                    - pictureStatus
                    - capableVoiceCall
                    - capableBuddy
                    - mid
                    - displayNameOverridden
                    - relation
                    - thumbnailUrl_
                    - createdTime
                    - facoriteTime
                    - capableMyhome
                    - attributes
                    - type
                    - phoneticName
                    - statusMessage
        """
        if type(ids) != list:
            msg = "argument should be list of contact ids"
            self.raise_error(msg)

        return self._client.getContacts(ids)

    def _createRoom(self, ids, seq=0):
        """Create a chat room"""
        return self._client.createRoom(seq, ids)

    def _getRoom(self, id):
        """Get a chat room"""
        return self._client.getRoom(id)

    def _inviteIntoRoom(self, roomId, contactIds=[]):
        """Invite contacts into room"""
        return self._client.inviteIntoRoom(0, roomId, contactIds)

    def _leaveRoom(self, id):
        """Leave a chat room"""
        return self._client.leaveRoom(0, id)

    def _createGroup(self, name, ids, seq=0):
        """Create a group"""
        return self._client.createGroup(seq, name, ids)

    def _getGroups(self, ids):
        """Get a list of group with ids"""
        if type(ids) != list:
            msg = "argument should be list of group ids"
            self.raise_error(msg)

        return self._client.getGroups(ids)

    def _getGroupIdsJoined(self):
        """Get group id that you joined"""
        return self._client.getGroupIdsJoined()

    def _getGroupIdsInvited(self):
        """Get group id that you invited"""
        return self._client.getGroupIdsInvited()

    def _acceptGroupInvitation(self, groupId, seq=0):
        """Accept a group invitation"""
        return self._client.acceptGroupInvitation(seq, groupId)

    def _cancelGroupInvitation(self, groupId, contactIds=[], seq=0):
        """Cancel a group invitation"""
        return self._client.cancelGroupInvitation(seq, groupId, contactIds)

    def _inviteIntoGroup(self, groupId, contactIds=[], seq=0):
        """Invite contacts into group"""
        return self._client.inviteIntoGroup(seq, groupId, contactIds)

    def _leaveGroup(self, id):
        """Leave a group"""
        return self._client.leaveGroup(0, id)

    def _getRecentMessages(self, id, count=1):
        """Get recent messages from `id`"""
        return self._client.getRecentMessages(id, count)

    def _sendMessage(self, message, seq=0):
        """Send a message to `id`. `id` could be contact id or group id

        :param message: `message` instance
        """
        return self._client.sendMessage(seq, message)

    def _getLastOpRevision(self):
        return self._client.getLastOpRevision()

    def _fetchOperations(self, revision, count=50):
        return self._client.fetchOperations(revision, count)

    def _getMessageBoxCompactWrapUp(self, id):
        try:
            return self._client.getMessageBoxCompactWrapUp(id)
        except:
            return None

    def _getMessageBoxCompactWrapUpList(self, start=1, count=50):
        try:
            return self._client.getMessageBoxCompactWrapUpList(start, count)
        except Exception as e:
            msg = e
            self.raise_error(msg)
    
    def raise_error(self, msg):
        """Error format"""
        raise Exception("Error: %s" % msg)

    def _get_json(self, url):
        """Get josn from given url with saved session and headers"""
        return json.loads(self._session.get(url, headers=self._headers).text)
