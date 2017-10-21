from django.contrib.auth.backends import RemoteUserBackend

class DummyRemoteUserBackend(RemoteUserBackend):

    def configure_user(self,user):
	"""Set user groups and privs. 
	This method is called the first time a non-django user logs in.
	A user is created in the django database, this method
	adds the new user to the appropriate groups, and 
	sets privs. """

	#all remote users are staff - so they can access the admin interface
	user.is_staff=True
	user.is_superuser=True

	user.save()
	return user
