import logging
import asyncio
import socket

import typing  #注意 typing 是 requirement.txt 里面的，需要额外安装

import sys
sys.path.append("..")
from module.cipher       import Cipher
from module.securesocket import SecureSocket
from utils               import net

Connection = socket.socket
logger = logging.getLogger(__name__)


class LsLocal(SecureSocket):
	# 新建一个本地端
	def __init__(self, loop: asyncio.AbstractEventLoop, password: bytearray, listenAddr: net.Address, remoteAddr: net.Address) -> None:
		super().__init__(loop=loop, cipher=Cipher.NewCipher(password))
		self.listenAddr = listenAddr
		self.remoteAddr = remoteAddr

	# 本地端启动监听，接收来自本机浏览器的连接
	async def listen(self, didListen: typing.Callable=None):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
			listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			listener.bind(self.listenAddr)
			listener.listen(socket.SOMAXCONN)
			listener.setblocking(False)

			logger.info('Listen to %s:%d' % self.listenAddr)
			if didListen:
				didListen(listener.getsockname())

			while True:
				connection, address = await self.loop.sock_accept(listener)
				logger.info('Receive %s:%d', *address)
				asyncio.ensure_future(self.handleConn(connection))

	async def handleConn(self, connection: Connection):
		remoteServer = await self.dialRemote()

		def cleanUp(task):
			"""
			Close the socket when they succeeded or had an exception.
			"""
			# 退出本次工作
			remoteServer.close()
			connection.close()

		# 从 localUser 读取数据发送到 dstServer
		local2remote = asyncio.ensure_future(self.decodeCopy(connection, remoteServer))
		# 从 localUser 发送数据发送到 proxyServer，这里因为处在翻墙阶段出现网络错误的概率更大
		remote2local = asyncio.ensure_future(self.encodeCopy(remoteServer, connection))
		task = asyncio.ensure_future(asyncio.gather(local2remote, remote2local, loop=self.loop, return_exceptions=True))
		task.add_done_callback(cleanUp)

	async def dialRemote(self):
		"""
		Create a socket that connects to the Remote Server.
		"""
		try:
			remoteConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			remoteConn.setblocking(False)
			await self.loop.sock_connect(remoteConn, self.remoteAddr)
		except Exception as err:
			raise ConnectionError('链接到远程服务器 %s:%d 失败:\n%r' % (*self.remoteAddr, err))

		return remoteConn
