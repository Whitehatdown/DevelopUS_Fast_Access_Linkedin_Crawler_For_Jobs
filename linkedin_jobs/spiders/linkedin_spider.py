import scrapy
from datetime import datetime, timedelta

#  Commands to run the spider
#  - scrapy crawl linkedin_jobs -a keywords="data analyst" -a location="India" -a post_timing="1 week"
#  - scrapy crawl linkedin_jobs -a keywords="data analyst" -a location="United States" -a post_timing="1 week"

class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    custom_settings = {
        'FEEDS': {
            'output/jobs_%(file_number)d_%(date)s.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&start='

    def __init__(self, keywords='python', location='India', *args, **kwargs):
        super(LinkedJobsSpider, self).__init__(*args, **kwargs)
        self.api_url = self.api_url.format(keywords=keywords, location=location)
        self.run_date = datetime.now().strftime("%Y%m%d")
        self.file_number = 1

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']
        job_item = {}
        jobs = response.css("li")
        num_jobs_returned = len(jobs)
        

        for job in jobs:
            job_title = job.css("h3::text").get(default='not-found').strip()
            job_detail_url = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            job_listed = job.css('time::text').get(default='not-found').strip()
            company_name = job.css('h4 a::text').get(default='not-found').strip()
            company_link = job.css('h4 a::attr(href)').get(default='not-found')
            company_location = job.css('.job-search-card__location::text').get(default='not-found').strip()

            # Filter jobs posted within the last week
            if self.is_posted_within_a_week(job_listed):
                job_item['job_title'] = job_title
                job_item['job_detail_url'] = job_detail_url
                job_item['job_listed'] = job_listed
                job_item['company_name'] = company_name
                job_item['company_link'] = company_link
                job_item['company_location'] = company_location
                yield job_item

        # Request the next page of jobs if there are more jobs available
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def is_posted_within_a_week(self, job_listed):
        now = datetime.now()
        if 'week' in job_listed or 'weeks' in job_listed:
            weeks_ago = int(job_listed.split()[0])
            if weeks_ago == 1:
                return True
        elif 'day' in job_listed or 'days' in job_listed:
            days_ago = int(job_listed.split()[0])
            if days_ago <= 7:
                return True
        return False