#!/usr/bin/env python3
"""Perform unit tests for the db_lib library."""

import os
import unittest

#from db_lib_editing import add_to_db_list, buffer_merges, insert_key, insert_key_large_value, select_key, select_key_large_value, select_random, setup_db
from db_lib import add_to_db_list, buffer_merges, insert_key, insert_key_large_value, select_key, select_key_large_value, select_random, setup_db

scratch_db = '/tmp/deleteme_unittest_db_lib.sqlite3'
archive_db = '/tmp/deleteme_unittest_db_lib_archive.sqlite3'
sha256_db = '/tmp/deleteme_unittest_db_lib_sha256.sqlite3'

class DbFunctionsTest(unittest.TestCase):
	"""Tests for the db_lib library."""

	def test001MakeDB(self):
		"""Set up the base databases."""
		for a_file in (scratch_db, scratch_db + '-shm', scratch_db + '-wal', archive_db, archive_db + '-shm', archive_db + '-wal', sha256_db, sha256_db + '-shm', sha256_db + '-wal'):
			if os.path.exists(a_file):
				os.remove(a_file)
		self.assertFalse(os.path.exists(scratch_db))
		self.assertFalse(os.path.exists(archive_db))
		self.assertFalse(os.path.exists(sha256_db))
		self.assertTrue(setup_db(scratch_db))
		self.assertTrue(setup_db(archive_db))

	def test002DbExists(self):
		"""Check that it's on disk."""
		self.assertTrue(os.path.exists(scratch_db))
		self.assertTrue(os.path.exists(archive_db))

	def test003AddKeys(self):
		"""Add a few keys."""
		self.assertTrue(insert_key(scratch_db, 'single_val_k1', ['v1a']))
		self.assertTrue(insert_key(scratch_db, 'single_val_k1', ['v1b']))
		self.assertTrue(insert_key(archive_db, 'archive_k11', ['v11c']))

	def test004CheckThere(self):
		"""See that they are in there."""
		self.assertEqual(select_key(scratch_db, 'single_val_k1'), ['v1b'])
		self.assertEqual(select_key(archive_db, 'archive_k11'), ['v11c'])
		self.assertEqual(select_key([scratch_db, archive_db], 'single_val_k1'), ['v1b'])
		#self.assertEqual(select_key(scratch_db, 'single_val_k1'), ['v1b'])
		self.assertEqual(select_key([scratch_db, archive_db], 'archive_k11'), ['v11c'])
		#self.assertEqual(select_key(archive_db, 'archive_k11'), ['v11c'])
		self.assertEqual(select_random(scratch_db), ('single_val_k1', ['v1b']))
		self.assertEqual(select_random(archive_db), ('archive_k11', ['v11c']))


	def test005AppendValue(self):
		"""Add new items to a row value."""
		self.assertTrue(add_to_db_list(scratch_db, 'single_val_k1', 'v1d'))
		self.assertEqual(select_key([scratch_db, archive_db], 'single_val_k1'), ['v1b', 'v1d'])
		#self.assertEqual(select_key(scratch_db, 'single_val_k1'), ['v1b', 'v1d'])

	def test006AddLarge(self):
		"""Make sure we can add large values across databases."""
		self.assertTrue(insert_key_large_value(scratch_db, [sha256_db], 'large21', 'val21f'))
		#self.assertTrue(insert_key_large_value(scratch_db, sha256_db, 'large21', 'val21f'))
		self.assertEqual(select_key_large_value([scratch_db], sha256_db, 'large21'), ['val21f'])
		#self.assertEqual(select_key_large_value(scratch_db, sha256_db, 'large21'), ['val21f'])
		self.assertEqual(select_key(scratch_db, 'large21'), ['9ba74ffd437c565d10019d2c9e93b03c4bdf10b2bedb1b93c509aeca2157f501'])	#sha256sum of 'val21f'
		self.assertEqual(select_key(sha256_db, '9ba74ffd437c565d10019d2c9e93b03c4bdf10b2bedb1b93c509aeca2157f501'), ['val21f'])

	def test007BufferedMerges(self):
		"""Test that buffering works correctly."""
		self.assertTrue(buffer_merges(scratch_db, 'k31', ['v31a'], 25))
		self.assertEqual(select_key(scratch_db, 'k31'), [])
		#self.assertEqual(select_key(scratch_db, 'k31'), None)
		self.assertTrue(buffer_merges('', 'k31', [], 0))
		self.assertEqual(select_key(scratch_db, 'k31'), ['v31a'])


	def test999Shutdown(self):
		"""Remove test files."""
		for a_file in (scratch_db, scratch_db + '-shm', scratch_db + '-wal', archive_db, archive_db + '-shm', archive_db + '-wal', sha256_db, sha256_db + '-shm', sha256_db + '-wal'):
			if os.path.exists(a_file):
				os.remove(a_file)
		self.assertFalse(os.path.exists(scratch_db))
		self.assertFalse(os.path.exists(archive_db))
		self.assertFalse(os.path.exists(sha256_db))

if __name__ == '__main__':
	unittest.main()
