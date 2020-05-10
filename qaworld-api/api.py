import settings
from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
import logging
from mongo import APIMongo
from random import random


class Team(Resource):

    def __init__(self):
        if app.testing:
            settings.MONGODB_NAME = settings.MONGODB_NAME_TEST
        self.data_source = APIMongo(settings)

    def get(self, tags):
        logging.info('[GET] Team {}'.format(tags))
        team = self.data_source.get_teams(self.get_tag_list(tags))
        if team is None:
            team = {}
        return team

    def post(self):
        # TODO Check tags existence
        tags = request.form.get('tags')
        name = request.form.get('name')
        # TODO Add current user as member
        logging.info('[POST] Team {}: {}'.format(name, tags))
        team = self.get_empty_team()
        team['tags'] = self.get_tag_list(tags)
        team['name'] = name
        self.data_source.save_team(team)

    @staticmethod
    def get_tag_list(tags_string):
        tag_list = tags_string.split(';')
        tag_list.sort()
        return tag_list

    @staticmethod
    def get_empty_team():
        return {
            'name': '',
            'id': str(random())[2:],
            'tags': [],
            'participants': [],
            'facts': {
                'num_posts': 0,
            },
            'last_updated': int(datetime.timestamp(datetime.utcnow())),
        }


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
api = Api(app)

prefix = '/v1'
api.add_resource(Team, '{}/teams/<tags>/'.format(prefix), endpoint='team')
api.add_resource(Team, '{}/teams/'.format(prefix), endpoint='teams')

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)