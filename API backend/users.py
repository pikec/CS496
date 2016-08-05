#!/usr/bin/env python
#
#Candis Pike
#API assignment CS496S'16
#code ideas adapted from lecture 

import webapp2
from google.appengine.ext import ndb
import db_models
import json

class UserHandler(webapp2.RequestHandler):
	def post(self):
		#create a new user - must be json format
		#Post Body:
		#name - required
		#email - required
		
		#check for proper data format
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
	
		#create a new user record
		name = self.request.get('name', default_value=None)
		email = self.request.get('email', default_value=None)
		new_user = db_models.User()
	
		#check that name and email are supplied
		if name:
			new_user.name = name
	
		else:
			self.response.set_status(400,"Invalid Request. Name of user required.")
			self.response.write(self.response.status)
			return
	
		if email:
			new_user.email = email
	
		else:
			self.response.set_status(400, "Invalid Request. Email of user required.")
			self.response.write(self.response.status)
			return
			
		#check if unique name and email
		#http://stackoverflow.com/questions/25728615/distinct-usernames-in-python-ndb
		#chk_key = ndb.Key('db_models.UserProj', name)
		#chk_use = chk_key.get()
		#if not chk_use:
		#	self.response.set_status(409,'User name exists.')
		#	self.response.write(self.response.status)
		#	return
				
		#all is good add to database
		key = new_user.put()
		out = new_user.to_dict()
		self.response.set_status(201, "New user created.")
		#self.response.write(self.response.status)
		self.response.write(json.dumps(out))
		return
	
	#get list of all user ids
	def get(self):
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
		#get user check that any user exists	
		q = db_models.User.query()
		name = q.fetch()
		if not name:
			self.response.set_status(400,"No users to display")
			self.response.write(self.response.status)
		else:	
			keys = q.fetch(keys_only=True)
			results = {'keys': [x.id() for x in keys], 'name': [x.name for x in name]}
			self.response.set_status(200)
			#self.response.write(self.response.status)	
			self.response.write(json.dumps(results))
		return
				
class OtherUserHandler(webapp2.RequestHandler):	
	#get user by id
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
			
		#get_by_id is quicker then .get() - from google
		results = db_models.User.get_by_id(int(kwargs['id']))
		if not results:
			self.response.set_status(404, "User not found.")
			self.response.write(self.response.status)	
		else:	
			out = results.to_dict()
			self.response.set_status(200)
			#self.response.write(self.response.status)	
			self.response.write(json.dumps(out))
		return
	
	#update user with id
	def put(self, **kwargs):
		#check for proper data format
		if 'application/json' not in self.request.accept:
			self.response.set_status(415, "Unsupported. API only supports application/json MIME type.")
			self.response.write(self.response.status)
			return
		
		#check for id
		if 'id' not in kwargs:
			self.response.set_status(400, "Invalid request. ID required.")
			self.response.write(self.response.status)
			return 
			
		#get id
		results = db_models.User.get_by_id(int(kwargs['id']))
		if not results:
			self.response.set_status(404, "User not found.")
			self.response.write(self.response.status)	
			return
		else:	
			new_name = self.request.get('name')
			new_email = self.request.get('email')
			
		if new_name:	
			results.name = new_name
		
		if new_email:
			results.email = new_email
			
		results.put()
		out = results.to_dict()
		self.response.set_status(200, "User updated.")
		#self.response.write(self.response.status)
		self.response.write(json.dumps(out))
		return
	
	#delete user with id	
	def delete(self, **kwargs):
		#can only delete an  id
		if 'id' not in kwargs:
			self.response.set_status(400, "Invalid request. ID required.")
			self.response.write(self.response.status)
			return 
		
		#check for valud id
		results = db_models.User.get_by_id(int(kwargs['id']))
		if not results:
			self.response.set_status(404, "User not found.")
			self.response.write(self.response.status)	
			return
		else:	
			#remove projects of user
			key = ndb.Key(db_models.User, int(kwargs['id']))
			list = db_models.Projects.query(db_models.Projects.user == key).fetch(keys_only=True)
			if list:
				ndb.delete_multi(list)
			#then remove user	
			results.key.delete()
			
			#check for success
			check = db_models.User.get_by_id(int(kwargs['id']))
			if check:
				self.response.set_status(500, "Server error. User not deleted.")
				self.response.write(self.response.status)
				return
			
			else:
				self.response.set_status(200, "User deleted.")
				#self.response.write(self.response.status)	
				return	
