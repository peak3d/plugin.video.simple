from ctypes import *


class AMediaDrmByteArray(Structure):
	_fields_ = [("ptr", c_char_p), ("length", c_ulong)]

class MediaDrm:
	def __init__(self):
		self.libMediaDrm = cdll.LoadLibrary('/system/lib/libmediandk.so')
		# Create MediaDrm with widevine UUID
		AMediaDrm_createByUUID = self.libMediaDrm.AMediaDrm_createByUUID
		self.mediaDrm = AMediaDrm_createByUUID('\xed\xef\x8b\xa9\x79\xd6\x4a\xce\xa3\xc8\x27\xdc\xd5\x1d\x21\xed')
		print 'MediaDrm Instance:' + hex(self.mediaDrm)

		# get the systemId property
		AMediaDrm_getPropertyString = self.libMediaDrm.AMediaDrm_getPropertyString
		self.systemId = c_char_p()
		status = AMediaDrm_getPropertyString(self.mediaDrm, 'systemId', byref(self.systemId))
		print 'MediaDrm systemId:' + self.systemId.value

	def openSession(self):
		AMediaDrm_openSession = self.libMediaDrm.AMediaDrm_openSession
		self.sessionId = AMediaDrmByteArray()
		status = AMediaDrm_openSession(self.mediaDrm, byref(self.sessionId))
		print 'MediaDrm sessionId: status:' + str(status) + ' ,size:' + str(self.sessionId.length)

        def closeSession(self):
		AMediaDrm_closeSession = self.libMediaDrm.AMediaDrm_closeSession
		status = AMediaDrm_closeSession(self.mediaDrm, byref(self.sessionId))
		print 'MediaDrm session closed status:' + str(status)
