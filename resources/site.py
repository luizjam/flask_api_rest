from flask_restful import Resource
from models.site import SiteModel
from flask_jwt_extended import jwt_required

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}
    
class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found.'}, 404 # not found
    
    def get_id(self, site_id):
        site = SiteModel.find_by_id(site_id)
        if site:
            return site.json()
        return None
    
    @jwt_required()
    def post(self, url):
        if SiteModel.find_site(url):
            return {"messge": "The site '{}' already exists.".format(url)}, 400 # bad request
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'An internal error ocurred trying to create a new site'}, 500
        return site.json()
    
    @jwt_required()
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}
        return {'message': 'Site not found.'}, 404