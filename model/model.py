# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from peewee import *
from playhouse.db_url import connect

import configparser

import os

config_path = "{}/config.ini".format(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read(config_path)

database = MySQLDatabase(config.get('DATABASE', 'dbname', fallback='test'),
            host=config.get('DATABASE', 'host', fallback='localhost'),
            user=config.get('DATABASE', 'user', fallback='user'),
            password=config.get('DATABASE', 'password', fallback='password'),
            )

class BaseModel(Model):
    class Meta:
        database = database
        db_table = 'course'

class Course(BaseModel):
    # course_id = UUIDField(primary_key=True)
    course_id = CharField(primary_key=True)
    course_title = CharField()
    course_description = TextField()
    language = CharField()
    level = CharField()
    student_enrolled = IntegerField()
    ratings = IntegerField()
    overall_rating = DecimalField()
    course_url = CharField()
    cover_image = CharField()
    source = CharField()

    def dictionary(self):
        data = {
                'course_id': "{0!s}".format(self.course_id),
                'course_title': "{0!s}".format(self.course_title),
                'course_description': "{0!s}".format(self.course_description),
                'language': "{0!s}".format(self.language),
                'level': "{0!s}".format(self.level),
                "student_enrolled": "{0!s}".format(self.student_enrolled),
                "ratings": "{0!s}".format(self.ratings),
                "overall_rating": "{0!s}".format(self.overall_rating),
                "course_url": "{0!s}".format(self.course_url),
                "cover_image": "{0!s}".format(self.cover_image),
                "source": self.source
                }

        return data

if __name__ == '__main__':
    if not Course.table_exists():
        Course.create_table()

