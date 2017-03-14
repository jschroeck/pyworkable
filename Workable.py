import requests
import json

class Workable(object):

    def __init__(self,account,apikey):
        self.account = str(account).lower()
        self.apikey = str(apikey)

        # Authorization headers. Content-Type is not necessary, but should workable start providing alternate
        # content types such as XML, this won't break
        self.request_headers = {
            'Content-Type': 'application/json',
            'authorization': 'Bearer ' + self.apikey
        }
        # Base URL Endpoint for all API requests
        self.api_base = 'https://www.workable.com/spi/v3/accounts/' + self.account + '/'

        # API Endpoints for all jobs, a single job, gettig a list of stages and account members
        self.endpoints = {
            'jobs':     self.api_base + 'jobs',
            'job':      self.api_base + 'jobs/',
            'stages':   self.api_base + 'stages/',
            'members':  self.api_base + 'members'
        }
        # Increase default limit for downloading lists from 50 to 100, so we need to make fewer requests
        self.default_limit = 100

#############################################################################################
#   Functions
#############################################################################################

    def workable_depaginate(self,url,key):
        """
        Returns one object based on a given key for a workable API endpoint.

        Arguments:
        url -- the API endpoint that returns paginated data
        key -- the key that contains all the data
        """
        list = []
        paging = True
        while paging == True:
            url = url + '?limit=' + str(self.default_limit)
            request = requests.get(url, headers=self.request_headers)
            response_json = request.json()
            list.extend(response_json[key])
            try:
                url = response_json['paging']['next'] + '?limit=' + self.default_limit
            except KeyError:
                paging = False
            else:
                paging = True
        return list

    def candidate_list(self,job):
        """
        Download and return the basic list of all candidates for a given job
        """
        job_candidates_url = self.endpoints['job'] + job + '/candidates'
        candidate_list = self.workable_depaginate(job_candidates_url,'candidates')
        return candidate_list


    def candidate_details(self,candidate_list,job):
        """
        Download and return Details for all candidates in a candidate_list
        """
        candidates = []

        for candidate in candidate_list:
            detail = single_candidate_detail(candidate['id'],job)
            candidates.append(detail['candidate'])
        return candidates

    def single_candidate_detail(self,candidate_id,job):
        """
        Returns the candidate's detail information, for a given candidate identified by ID
        """
        url = self.endpoints['job'] + job + '/candidates/' + candidate_id
        request = requests.get(url,headers=self.request_headers)
        response = request.json()
        return response

    def job_list(self,state=''):
        """
        Returns a list of all jobs matching the given state
        :param state: one of the following: draft, published, archived, closed
        :return: Job List
        """
        jobs = []
        if state != '':
            url = self.endpoints['jobs'] + '?state=' + state
        else:
            url = self.endpoints['jobs']
        jobs = self.workable_depaginate(url,'jobs')
        return jobs

    def job_detail(self,job):
        """
        Returns detail info for a given job
        :param job: Job Shortcode
        :return: Job Info
        """
        url = self.endpoints['job'] + job
        request = requests.get(url,headers=self.request_headers)
        job = request.json()
        return job
