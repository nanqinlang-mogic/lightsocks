########################################################
# 再使用 cipher.py 去封装一个加密传输的 SecureSocket，以方便直接加解密 TCP Socket 中的流式数据（data flow）
# 这个 SecureSocket 用于 local 端和 server 端之间进行 TCP 通信，并且只使用 SecureSocket 通信时中间传输的数据会被加密，防火墙无法读到原数据
########################################################


import logging
import socket
import asyncio

# from . import cipher 或 import cipher
# 这里只要 cipher.py 中的 Class "Cipher"
from .cipher import Cipher

BUFFER_SIZE = 1024
Connection = socket.socket
logger = logging.getLogger(__name__)


class SecureSocket:
	"""
	SecureSocket is a socket,
	that has the ability to decode read and encode write.
	"""

	# 加密传输的 TCP Socket
	def __init__(self, loop: asyncio.AbstractEventLoop, cipher: Cipher) -> None:
		self.loop = loop or asyncio.get_event_loop()
		self.cipher = cipher

	# 从输入流里读取加密过的数据，解密后把原数据放到 bs 里
	async def decodeRead(self, conn: Connection):
		data = await self.loop.sock_recv(conn, BUFFER_SIZE)

		logger.debug('%s:%d decodeRead %r', *conn.getsockname(), data)

		bs = bytearray(data)
		self.cipher.decode(bs)
		return bs

	# 把放在 bs 里的数据加密后立即全部写入输出流
	async def encodeWrite(self, conn: Connection, bs: bytearray):
		logger.debug('%s:%d encodeWrite %s', *conn.getsockname(), bytes(bs))

		bs = bs.copy()

		self.cipher.encode(bs)
		await self.loop.sock_sendall(conn, bs)

	# 从 src（source） 中源源不断的读取原数据，加密后写入到 dst（destination），直到 src 中没有数据可以再读取
	async def encodeCopy(self, dst: Connection, src: Connection):
		"""
		It encodes the data flow from the src and sends to dst.
		"""

		logger.debug('encodeCopy %s:%d => %s:%d', *src.getsockname(), *dst.getsockname())

		while True:
			data = await self.loop.sock_recv(src, BUFFER_SIZE)
			if not data:
				break
			await self.encodeWrite(dst, bytearray(data))

	# 从 src 中源源不断的读取加密后的数据，解密后写入到 dst，直到 src 中没有数据可以再读取
	async def decodeCopy(self, dst: Connection, src: Connection):
		"""
		It decodes the data flow from the src and sends to dst.
		"""

		logger.debug('decodeCopy %s:%d => %s:%d',
					 *src.getsockname(), *dst.getsockname())

		while True:
			bs = await self.decodeRead(src)
			if not bs:
				break
			await self.loop.sock_sendall(dst, bs)
