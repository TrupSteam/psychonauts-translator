#python2


import os
import sys
import struct
import argparse


'''
Replaces old lines inside a *.LUB file with new ones from a *.CSV file

Example: python replace_strings.py AS_StringTable.lub AS_StringTable.csv AS_StringTable_new.lub
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


class LUB_PATCHER:
	
	def __init__(self):
		self.csv_list = []
		self.lub_data = None
		self.counter = 0
		
	def show_result(self):
		print('Replaced {} string(s)'.format(self.counter))
		
	def replace(self, lub_path, csv_path, out_path):
		self.read_csv(csv_path)
		self.read_lub(lub_path)
		self.actual_work()
		save_binary(out_path, self.lub_data)
		self.show_result()

	def read_csv(self, csv_path):
		data = read_binary(csv_path)
		for str in data.split('\r\n'):
			if not str: continue
			self.csv_list.append([str[:9], str[10:]])

	def read_lub(self, lub_path):
		self.lub_data = read_binary(lub_path)
		
	def replace_in_lub(self, offset, size, new_str):
		self.lub_data = self.lub_data[:offset] + new_str + self.lub_data[offset + size -1:]
		self.counter += 1
		
	def get_size_of_lua_str(self, offset):
		bin_size = self.lub_data[offset:4 + offset]
		int_size = struct.unpack('L', bin_size)
		if not int_size: return False
		full_size = int_size[0] + 4 + 1
		return full_size
	
	def get_old_string(self, str_id):
		offset = self.lub_data.find(str_id)
		if offset == -1: return False
		offset += len(str_id) + 1
		str_size = self.get_size_of_lua_str(offset)
		return [offset, str_size]

	def build_lua_str(self, str_data):
		size = struct.pack('L', len(str_data) + 1)
		return size + str_data + '\x00'
		
	def actual_work(self):
		for csv in self.csv_list:
			if len(csv[1]) == 0: continue
			old_str = self.get_old_string(csv[0])
			if not old_str: raise ValueError('Unknown string - ' + csv[0])
			new_str = self.build_lua_str(csv[1])
			self.replace_in_lub(old_str[0], old_str[1], new_str)
		
		
##############################################################	


if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(description='Replaces old lines inside a *.LUB file with new ones from a *.CSV file')
	arg_parser.add_argument('lub_path')
	arg_parser.add_argument('csv_path') 
	arg_parser.add_argument('out_path')
	args = arg_parser.parse_args()
	lub_parser = LUB_PATCHER()
	lub_parser.replace(args.lub_path, args.csv_path, args.out_path)
	
		
		
		