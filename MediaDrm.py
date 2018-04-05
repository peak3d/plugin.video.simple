from ctypes import *


class AMediaDrmByteArray(Structure):
	_fields_ = [("ptr", c_char_p), ("length", c_ulong)]

class MediaDrm:

	KEY_TYPE_STREAMING = c_int(1)
	KEY_TYPE_OFFLINE = c_int(2)
	KEY_TYPE_RELEASE = c_int(3)

	def __init__(self):
		self.libMediaDrm = cdll.LoadLibrary('/system/lib/libmediandk.so')
		# Create MediaDrm with widevine UUID
		AMediaDrm_createByUUID = self.libMediaDrm.AMediaDrm_createByUUID
		self.mediaDrm = AMediaDrm_createByUUID('\xed\xef\x8b\xa9\x79\xd6\x4a\xce\xa3\xc8\x27\xdc\xd5\x1d\x21\xed')
		print 'MediaDrm Instance:' + hex(self.mediaDrm)

		# get the systemId property
		AMediaDrm_getPropertyString = self.libMediaDrm.AMediaDrm_getPropertyString
		self.systemId = c_char_p()
		self.sessionStatus = AMediaDrm_getPropertyString(self.mediaDrm, 'systemId', byref(self.systemId))
		print 'MediaDrm systemId:' + self.systemId.value

	def openSession(self):
		if self.sessionStatus != 0:
			return False
		AMediaDrm_openSession = self.libMediaDrm.AMediaDrm_openSession
		self.sessionId = AMediaDrmByteArray()
		status = AMediaDrm_openSession(self.mediaDrm, byref(self.sessionId))
		print 'MediaDrm sessionId: status:' + str(status) + ', size:' + str(self.sessionId.length)
		return status == 0

        def closeSession(self):
		AMediaDrm_closeSession = self.libMediaDrm.AMediaDrm_closeSession
		status = AMediaDrm_closeSession(self.mediaDrm, byref(self.sessionId))
		print 'MediaDrm session closed status:' + str(status)

	def getKeyRequest(self, data):
		AMediaDrm_getKeyRequest = self.libMediaDrm.AMediaDrm_getKeyRequest
		self.keyRequest = c_char_p()
		self.keyRequestSize = c_ulong()
		status = AMediaDrm_getKeyRequest(
			self.mediaDrm,
			byref(self.sessionId),
			cast(data, c_char_p),
			c_ulong(len(data)),
			'',
			self.KEY_TYPE_OFFLINE,
			None,
			0,
			byref(self.keyRequest),
			byref(self.keyRequestSize))
		print 'MediaDrm getKeyRequest returnes status:' + str(status) + ', size:' + str(self.keyRequestSize)
