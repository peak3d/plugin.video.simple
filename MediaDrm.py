from ctypes import *


class AMediaDrmByteArray(Structure):
	_fields_ = [("ptr", c_char_p), ("length", c_ulong)]

class MediaDrm:

	KEY_TYPE_STREAMING = c_int(1)
	KEY_TYPE_OFFLINE = c_int(2)
	KEY_TYPE_RELEASE = c_int(3)


	AMEDIA_OK = 0
	AMEDIA_ERROR_BASE = -10000
	AMEDIA_ERROR_UNKNOWN = AMEDIA_ERROR_BASE
	AMEDIA_ERROR_MALFORMED = AMEDIA_ERROR_BASE - 1
	AMEDIA_ERROR_UNSUPPORTED = AMEDIA_ERROR_BASE - 2
	AMEDIA_ERROR_INVALID_OBJECT = AMEDIA_ERROR_BASE - 3
	AMEDIA_ERROR_INVALID_PARAMETER = AMEDIA_ERROR_BASE - 4
	AMEDIA_ERROR_INVALID_OPERATION = AMEDIA_ERROR_BASE - 5
	AMEDIA_DRM_ERROR_BASE = -20000
	AMEDIA_DRM_NOT_PROVISIONED = AMEDIA_DRM_ERROR_BASE - 1
	AMEDIA_DRM_RESOURCE_BUSY = AMEDIA_DRM_ERROR_BASE - 2
	AMEDIA_DRM_DEVICE_REVOKED = AMEDIA_DRM_ERROR_BASE - 3
	AMEDIA_DRM_SHORT_BUFFER = AMEDIA_DRM_ERROR_BASE - 4
	AMEDIA_DRM_SESSION_NOT_OPENED = AMEDIA_DRM_ERROR_BASE - 5
	AMEDIA_DRM_TAMPER_DETECTED = AMEDIA_DRM_ERROR_BASE - 6
	AMEDIA_DRM_VERIFY_FAILED = AMEDIA_DRM_ERROR_BASE - 7
	AMEDIA_DRM_NEED_KEY = AMEDIA_DRM_ERROR_BASE - 8
	AMEDIA_DRM_LICENSE_EXPIRED = AMEDIA_DRM_ERROR_BASE - 9

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
		print 'MediaDrm sessionId open: status:' + str(status) + ', size:' + str(self.sessionId.length)
		return status == self.AMEDIA_OK

	def closeSession(self):
		AMediaDrm_closeSession = self.libMediaDrm.AMediaDrm_closeSession
		status = AMediaDrm_closeSession(self.mediaDrm, byref(self.sessionId))
		print 'MediaDrm session closed: status:' + str(status)

	def getKeyRequest(self, data):
		AMediaDrm_getKeyRequest = self.libMediaDrm.AMediaDrm_getKeyRequest
		keyRequestPtr = c_char_p()
		keyRequestLength = c_ulong()
		status = AMediaDrm_getKeyRequest(
			self.mediaDrm,
			byref(self.sessionId),
			cast(data, c_char_p),
			c_ulong(len(data)),
			'',
			self.KEY_TYPE_OFFLINE,
			None,
			0,
			byref(keyRequestPtr),
			byref(keyRequestLength))
		print 'MediaDrm getKeyRequest status:' + str(status) + ', size:' + str(keyRequestLength)

		if status == self.AMEDIA_DRM_NOT_PROVISIONED:
			#TODO: Make provisioning request
			pass
		return AMediaDrmByteArray(keyRequestPtr, keyRequestLength)

	def provideKeyResponse(self, data):
		if len(data) == 0:
			return false
		AMediaDrm_provideKeyResponse = self.libMediaDrm.AMediaDrm_provideProvisionResponse()
		self.keySetId = AMediaDrmByteArray()

		status = AMediaDrm_provideKeyResponse(self.mediaDrm, byref(self.sessionId), cast(data, c_char_p), c_ulong(len(data)), byref(self.keySetId))

		return status == self.AMEDIA_OK

	def decrypt(self, keyId, iv, data):
		AMediaDrm_decrypt = self.libMediaDrm.AMediaDrm_decrypt
		resultBuffer = bytes(len(data))
		status = AMediaDrm_decrypt(self.mediaDrm,
			byref(self.sessionId),
			'AES/CBC/NoPadding',
			cast(keyId, c_char_p),
			cast(iv, c_char_p),
			cast(data, c_char_p),
			cast(resultBuffer, c_char_p),
			cast(len(data), c_ulong))
		print 'MediaDrm decrypt status:' + str(status)

		return resultBuffer

	def encrypt(self, keyId, iv, data):
		AMediaDrm_encrypt = self.libMediaDrm.AMediaDrm_encrypt
		resultBuffer = bytes(len(data))
		status = AMediaDrm_encrypt(self.mediaDrm,
			byref(self.sessionId),
			'AES/CBC/NoPadding',
			cast(keyId, c_char_p),
			cast(iv, c_char_p),
			cast(data, c_char_p),
			cast(resultBuffer, c_char_p),
			cast(len(data), c_ulong))
		print 'MediaDrm encrypt status:' + str(status)

		return resultBuffer

	def sign(self, message):
		AMediaDrm_sign = self.libMediaDrm.AMediaDrm_sign

		signaturePtr = c_char_p()
		signatureLength = c_ulong()
		status = AMediaDrm_sign(self.mediaDrm,
			byref(self.sessionId),
			'JcaAlgorithm.HMAC_SHA256',
                        cast(message, c_char_p),
			cast(len(message), c_ulong),
			signaturePtr,
			signatureLength)
		print 'MediaDrm sign status:' + str(status) + ', signature length:' + str(signatureLength)

		return AMediaDrmByteArray(signaturePtr, signatureLength)

	def verify(self, message, signature):
		AMediaDrm_verify = self.libMediaDrm.AMediaDrm_verify
		status = AMediaDrm_verify(self.mediaDrm,
			byref(self.sessionId),
			'JcaAlgorithm.HMAC_SHA256',
			cast(message, c_char_p),
			cast(len(message), c_ulong),
			cast(signature, c_char_p),
			cast(len(signature), c_ulong))
		print 'MediaDrm verify status:' + str(status)

		return status == self.AMEDIA_OK
