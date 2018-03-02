########################################################
# 对数据进行加密解密
########################################################


class Cipher:
	"""
		Cipher class is for the encipherment of data flow.
		One octet is in the range 0 ~ 255 (2 ^ 8).
		To do encryption, it just maps one byte to another one.
		Example:
			encodePassword
			| index | 0x00 | 0x01 | 0x02 | 0x03 | ... | 0xff | || 0x02ff0a04
			| ----- | ---- | ---- | ---- | ---- | --- | ---- | ||
			| value | 0x01 | 0x02 | 0x03 | 0x04 | ... | 0x00 | \/ 0x03000b05
			decodePassword
			| index | 0x00 | 0x01 | 0x02 | 0x03 | 0x04 | ... | || 0x03000b05
			| ----- | ---- | ---- | ---- | ---- | ---- | --- | ||
			| value | 0xff | 0x00 | 0x01 | 0x02 | 0x03 | ... | \/ 0x02ff0a04
		It just shifts one step to make a simply encryption, encode and decode.
	"""

	def __init__(self, encodePassword: bytearray, decodePassword: bytearray) -> None:
		# 编码用的密码
		self.encodePassword = encodePassword.copy()
		# 解码用的密码
		self.decodePassword = decodePassword.copy()

	# 加密原数据
	def encode(self, bs: bytearray):
		for i, v in enumerate(bs):
			bs[i] = self.encodePassword[v]

	# 解码加密后的数据到原数据
	def decode(self, bs: bytearray):
		for i, v in enumerate(bs):
			bs[i] = self.decodePassword[v]

	@classmethod
	# 新建一个编码解码器
	def NewCipher(cls, encodePassword: bytearray):
		decodePassword = encodePassword.copy()

		for i, v in enumerate(encodePassword):
			decodePassword[v] = i

		return cls(encodePassword, decodePassword)
