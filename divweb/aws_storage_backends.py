from storages.backends.s3boto3 import S3Boto3Storage as SBS
class StaticStorage(SBS):
	location = 'static'


class PrivateMediaImageStorage(SBS):
	location = 'media/authors/images'
	file_overwrite = False

class PublicMediaImageStorage(SBS):
	location = 'media/website/images'
	default_acl = 'private'
	file_overwrite = False
	custom_domain = False