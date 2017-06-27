# -*- coding:utf-8 -*-

import unittest
from squan_blog.models import User


class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		user_test = User(password='TheAnswer')
		self.assertTrue(user_test.password_hash is not None)


	def test_no_password_getter(self):
		user_test = User(password='TheAnswer')
		with self.assertRaises(AttributeError):
			user_test.password


	def test_password_verification(self):
		user_test = User(password='TheAnswer')
		self.assertTrue(user_test.verify_password('TheAnswer'))
		self.assertFalse(user_test.verify_password('SomeoneElse'))


	def test_password_diff_from_others(self):
		user_test01 = User(password='TheAnswer')
		user_test02 = User(password='TheAnswer')
		self.assertTrue(user_test01.password_hash != user_test02.password_hash)
