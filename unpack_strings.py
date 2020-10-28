#python2


import struct
import sys
import os
import re
import argparse


'''
Convert *.LUB files (compiled lua4) to *.CSV (plain text) files

Based on "lua_src_4\src\luac\dump.c" & "lua_src_4\src\luac\lobject.h"

Example: python unpack_strings.py AS_StringTable.lub 
'''


##############################################################	


def read_binary(path):
	with open(path, "rb") as f:
		return f.read()
	return False
	
def save_binary(path, data):
	with open(path, "wb") as f:
		return f.write(data)
	return False
	
	
##############################################################	


class FileReader:

	def __init__(self, data):
		self.offset = 0
		self.data = data
		
	def skip(self, size):
		self.offset += size
		
	def read(self, size):
		#print('read {}:{}'.format(self.offset, size))
		out = self.data[self.offset : self.offset + size]
		self.skip(size)
		return out
		
	def read_int32(self):
		return struct.unpack('<I', self.read(4))[0]
	
	def read_byte(self):
		return struct.unpack('B', self.read(1))[0]
	
	def read_sign(self):
		return struct.unpack('<4s', self.read(4))[0]

		
##############################################################	

	
class LuaHeader:
	
	def __init__(self, data):
		self.signature = data.read_sign()
		self.version = data.read_byte()
		self.endian = data.read_byte()
		self.size_int = data.read_byte()
		self.size_size_t = data.read_byte()
		self.size_of_Instruction = data.read_byte()
		self.SIZE_INSTRUCTION = data.read_byte()
		self.SIZE_OP = data.read_byte()
		self.SIZE_B = data.read_byte()
		self.sizeof_number = data.read_byte()
		data.skip(self.sizeof_number * 1)
		
	def valid_sign(self):
		return (self.signature == '\x1bLua')
	
	def valid_version(self):
		return (self.version == 0x40)
	
		
class LuaString:
	
	def __init__(self, data):
		self.size = data.read_int32()
		self.str = data.read(self.size)
		
	def __repr__(self):
		#skip zero
		return self.str.rstrip('\x00')
	
	
class LocalOne:
	
	def __init__(self, data):
		self.name = LuaString(data)
		self.startpc = data.read_int32()
		self.endpc = data.read_int32()


class LocalsAll:
	
	def __init__(self, data):
		loc_vars = data.read_int32()
		self.vars = []
		for i in range(loc_vars):
			self.vars.append(LocalOne(data))

			
class LuaLines:
	
	def __init__(self, data):
		nlineinfo = data.read_int32()
		data.skip(nlineinfo * 4)
	
	
class LuaCode:
	
	def __init__(self, data):
		global header
		ncode = data.read_int32()
		if ncode == 0: return
		data.skip(header.SIZE_INSTRUCTION / 8 * ncode) 

	
class LuaConstants:
	
	def __init__(self, data):
		# strings used by the function 
		self.str = []
		str_count = data.read_int32()
		for i in range(str_count):
			self.str.append(LuaString(data))
			
		# numbers used by the function
		num_count = data.read_int32()
		data.skip(num_count * 4)
		
		# functions defined inside the function
		self.func = []
		func_count = data.read_int32()
		for i in range(func_count):
			self.func.append(LuaFunction(data))
	

class LuaFunction:
	
	def __init__(self, data):
		self.name = LuaString(data)
		data.skip(0xD) # func args
		self.locals = LocalsAll(data)
		self.lines = LuaLines(data)
		self.const = LuaConstants(data)
		self.code = LuaCode(data)

		
##############################################################	

class LUB_PARSER:

	def __init__(self):
		self.str = []
		self.re_str_id = re.compile('[0-9A-Z]{9}')

	def show_result(self):
		print('Parsed {} string(s)'.format(len(self.str)))
		
	def parse(self, path):
		bin = read_binary(path)
		reader = FileReader(bin)
		self.parse_data(reader)
		self.save_csv(path)
		self.show_result()
		
	def parse_data(self, data):
		global header
		header = LuaHeader(data)
		
		if not header.valid_sign():
			raise ValueError('Invalid LUB Signature')
			
		if not header.valid_version():
			raise ValueError('Invalid LUB Version')
		
		func = LuaFunction(data)
		self.parse_func(func)
		
	def is_lua_str_id(self, string):
		return self.re_str_id.match(string)
		
	def parse_func(self, func):
		self.parse_func_str(func)
		
		for ffnc in func.const.func:
			self.parse_func(ffnc)
		
	def parse_func_str(self, func):
		last_id = None
		
		for fstr in func.const.str:
		
			fstr = str(fstr)
	
			if last_id is None:
				if self.is_lua_str_id(fstr):
					last_id = fstr
			else:
				if not self.is_lua_str_id(fstr):
					# fstr.replace('\r', '') ?
					final_str = '{};{}'.format(last_id, fstr)
					self.str.append(final_str)
					last_id = None
				else:
					last_id = fstr
					continue

	def save_csv(self, path):
		str_data = '\r\n'.join(self.str)
		new_path = path[:-4] + '.csv'
		save_binary(new_path, str_data)

	
##############################################################	


if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(description='Convert *.LUB files (compiled lua4) to *.CSV (plain text) files')
	arg_parser.add_argument('lub_file_path')
	args = arg_parser.parse_args()
	# check is valid
	lub_parser = LUB_PARSER()
	lub_parser.parse(args.lub_file_path)


