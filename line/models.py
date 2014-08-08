# -*- coding: utf-8 -*-
"""
    line.models
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime
from curve.ttypes import Message, ContentType

class LineMessage:
    """LineMessage wrapper"""

    def __init__(self, client, message):
        self._client = client
        self.id   = message.id
        self.text = message.text

        self.hasContent = message.hasContent
        self.contentType = message.contentType
        self.contentPreview = message.contentPreview
        self.contentMetadata = message.contentMetadata
        
        self.sender   = client.getContactOrRoomOrGroupById(message._from)
        self.receiver = client.getContactOrRoomOrGroupById(message.to)

        # toType
        # 0: User
        # 1: Room
        # 2: Group
        self.toType = message.toType
        self.createdTime = datetime.fromtimestamp(message.createdTime/1000)

    def __repr__(self):
        return 'LineMessage (contentType=%s, sender=%s, receiver=%s, msg="%s")' % (
                    ContentType._VALUES_TO_NAMES[self.contentType],
                    self.sender,
                    self.receiver,
                    self.text
                )

class LineBase(object):
    _messageBox = None

    def sendMessage(self, text):
        """Send a message
        
        :param text: text message to send
        """
        try:
            message = Message(to=self.id, text=text)
            self._client.sendMessage(message)

            return True
        except Exception as e:
            raise e

    def sendSticker(self,
                    stickerId = "13",
                    stickerPackageId = "1",
                    stickerVersion = "100",
                    stickerText="[null]"):
        """Send a sticker
        
        :param stickerId: id of sticker
        :param stickerPackageId: package id of sticker
        :param stickerVersion: version of sticker
        :param stickerText: text of sticker (default='[null]')
        """
        try:
            message = Message(to=self.id, text="")
            message.contentType = ContentType.STICKER

            message.contentMetadata = {
                'STKID': stickerId,
                'STKPKGID': stickerPackageId,
                'STKVER': stickerVersion,
                'STKTXT': stickerText,
            }

            self._client.sendMessage(message)

            return True
        except Exception as e:
            raise e

    def sendImage(self, path):
        """Send a image
        
        :param path: local path of image to send
        """
        try:
            img = open(path, 'r')

            message = Message(to=self.id, text=text)
            message.contentType = ContentType.IMAGE
            message.contentPreview = img.read().encode('utf-8')

            self.raise_error("not implemented yet")

            url = None

            message.contentMetadata = {
                'PREVIEW_URL': url,
                'DOWNLOAD_URL': url,
                'PUBLIC': True,
            }

            self._client.sendMessage(message)

            return True
        except Exception as e:
            raise e

    def sendImageWithURL(self, url):
        """Send a image with given image url

        :param url: image url to send
        """
        try:
            response = requests.get(url, stream=True)

            message = Message(to=self.id, text=None)
            message.contentType = ContentType.IMAGE
            message.contentPreview = response.raw.read()
            #message.contentPreview = url.encode('utf-8')

            message.contentMetadata = {
                'PREVIEW_URL': url,
                'DOWNLOAD_URL': url,
                'PUBLIC': "True",
            }

            self._client.sendMessage(message, seq=1)

            return True
        except Exception as e:
            raise e

    def getRecentMessages(self, count=1):
        """Get recent messages
        
        :param count: count of messages to get
        """
        if self._messageBox:
            messages = self._client.getRecentMessages(self._messageBox, count)

            return messages
        else:
            self._messageBox = self._client.getMessageBox(self.id)
            messages = self._client.getRecentMessages(self._messageBox, count)

            return messages

    def __lt__(self, other):
        return self.id < other.id

class LineGroup(LineBase):
    """LineGroup wrapper

    Attributes:
        creator     contact of group creator
        members     list of contact of group members
        invitee     list of contact of group invitee

    >>> group = LineGroup(client, client.groups[0])
    """

    id        = None
    name      = None
    is_joined = True

    creator = None
    members = []
    invitee = []

    def __init__(self, client, group=None, is_joined=True):
        """LineGroup init

        :param client: LineClient instance
        :param group: Group instace
        :param is_joined: is a user joined or invited to a group
        """

        self._group  = group

        self.id      = group.id
        self.name    = group.name

        self.is_joined = is_joined

        try:
            self.creator = LineContact(client, group.creator)
        except:
            self.creator = None

        self.members = []
        for member in group.members:
            self.members.append(LineContact(client, member))

        self.invitee = []
        if group.invitee:
            for member in group.invitee:
                self.invitee.append(LineContact(client, member))

    def acceptGroupInvitation(self):
        if not self.is_joined:
            self._client.acceptGroupInvitation(self)
            
            return True
        else:
            raise Exception('You are already in group')

            return False

    def leave(self):
        """Leave group"""
        if self.is_joined:
            try:
                self.leaveGroup(self)
                return True
            except:
                return False
        else:
            raise Exception('You are not joined to group')
            return False

    def getMemberIds(self):
        """Get member ids of group"""
        ids = [member.id for member in self.members]

        return ids

    def __repr__(self):
        """Name of Group and number of group members"""
        if self.is_joined:
            return '<LineGroup %s #%s>' % (self.name, len(self.members))
        else:
            return '<LineGroup %s #%s (invited)>' % (self.name, len(self.members))

class LineRoom(LineBase):
    """Chat room wrapper

    Attributes:
        contacts           Contact list of chat room
    """
    def __init__(self, client, room):
        """LineContact init

        :param client: LineClient instance
        :param room: Room instace
        """

        self._client  = client
        self._room = room

        self.id = room.mid

        self.contacts = []
        for contact in room.contacts:
            self.contacts.append(LineContact(client, contact))

    def leave(self):
        """Leave room"""
        try:
            self.leaveRoom(self)

            return True
        except:
            return False

    def invite(self, contact):
        """Invite into group
        
        :param contact: LineContact instance to invite
        """


    def getContactIds(self):
        """Get contact ids of room"""
        ids = [contact.id for contact in self.contacts]

        return ids

    def __repr__(self):
        return '<LineRoom %s>' % (self.contacts)

class LineContact(LineBase):
    """LineContact wrapper

    Attributes:
        name            display name of contact
        statusMessage   status message of contact
    """
    def __init__(self, client, contact):
        """LineContact init

        :param client: LineClient instance
        :param contact: Conatct instace
        """

        self._client  = client
        self._contact = contact

        self.id            = contact.mid
        self.name          = contact.displayName
        self.statusMessage = contact.statusMessage

    @property
    def rooms(self):
        """Rooms that contact participates"""
        rooms = []

        for room in self._client.rooms:
            if self.id in room.getContactIds():
                rooms.append(room)

        return rooms

    @property
    def groups(self):
        """Groups that contact participates"""
        groups = []

        for group in self._client.groups:
            if self.id in group.getMemberIds():
                groups.append(room)

        return groups

    def __repr__(self):
        #return '<LineContact %s (%s)>' % (self.name, self.id)
        return '<LineContact %s>' % (self.name)
