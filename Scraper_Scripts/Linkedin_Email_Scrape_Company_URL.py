
import requests
import re
import csv
import os
from time import sleep


s = requests.Session()
company_link = "https://www.linkedin.com/company/gap-inc--gap/"  # target company link
output_file_name = "leads.csv"  # output CSV excel file name
pagination_delay = 5  # delay in seconds before going to the next page
cookies = 'JSESSIONID="ajax:0802970957117886885"; bcookie="v=2&d13db320-8f91-4586-858f-c977d6565beb"; bscookie="v=1&20221119125229a7e62bb8-0905-49c3-8aa1-75227d152281AQHwrB3TamNYli48j89v071XcQ-rXMia"; liap=true; dfpfpt=24033068ce344fc999faa5280196f000; _guid=3b0e40d2-664d-4ebc-8354-24d1d4021ad6; li_sugr=5be1011b-7b38-408b-a523-6dd497d4a9dd; VID=V_2024_04_14_18_1832; timezone=Asia/Calcutta; li_theme=light; li_theme_set=app; _gcl_au=1.1.1612355788.1717768004; AnalyticsSyncHistory=AQIBbHIMEfqhRgAAAY_3esXFceaPfiZNjtUZRo7GRz6XiQF5iYAtidbc5rl9eaYTTQEs4ziuw3hEphXmd7Kp1w; lms_ads=AQGCRBbOkahYygAAAY_3eswKap87vX25bFQEO6Q4lDRp6JXnn8aXyjZMEiAJDyEu9NFoytERRQLCukFUZqw2aaFEY0kvbQ8t; lms_analytics=AQGCRBbOkahYygAAAY_3eswKap87vX25bFQEO6Q4lDRp6JXnn8aXyjZMEiAJDyEu9NFoytERRQLCukFUZqw2aaFEY0kvbQ8t; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; gpv_pn=www.linkedin.com%2Fcompany%2Fid-redacted%2Fadmin%2Fdashboard%2F; s_plt=9.37; s_pltp=www.linkedin.com%2Fcompany%2Fid-redacted%2Fadmin%2Fdashboard%2F; s_cc=true; s_ips=639.9538462162018; s_tp=637; s_ppv=www.linkedin.com%2Fcompany%2Fid-redacted%2Fadmin%2Fdashboard%2F%2C874%2C100%2C5568%2C1%2C1; s_tslv=1717932987695; s_sq=lnkdprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwww.linkedin.com%25252Fcompany%25252Fid-redacted%25252Fadmin%25252Fdashboard%25252F%2526link%253DMessaging%2526region%253Dglobal-nav%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwww.linkedin.com%25252Fcompany%25252Fid-redacted%25252Fadmin%25252Fdashboard%25252F%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.linkedin.com%25252Fmessaging%25252F%25253F%2526ot%253DA; fptctx2=taBcrIH61PuCVH7eNCyH0FFaWZWIHTJWSYlBtG47cVt9qy64S3XgPFbIJj2sQAYM9W6MX%252bb7tdmtA2CLCAJ3MzHcFHeEDmG2vS99aoFPbLBRr%252bOfNuoJds2%252fjnHugC3U%252f2SCxfsmSK7vKcKXW%252fYvdEXqfg1JCiOMrtkL0UzcK5s1sTv2lMuZgs2%252fF8GKOrPWs2MCCYDWDJc%252bzNTnWgeF7OUmVfdVSC2Rs2p9GGbggopiBlFTLzlvGfcZcUvhflbL%252fxX7vWN95pmGg%252flE9tRheZQfDuh8N3jkJvXMXcoeUuSQi81D2tjFKDBe1XjvI8GdxpfreDUH4LIzkp9L64RcUD54GmG3gKd0kLhfKcyookU%253d; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImZsb3dUcmFja2luZ0lkIjoiYnJYM01XWTJSMEc2b1dFTE5VdG1Ydz09In0sIm5iZiI6MTcxODAxNjA0MSwiaWF0IjoxNzE4MDE2MDQxfQ.OloJUcn-JTuboYTrMaTAzqDbX7hEfnhd7rka2uSSHoI; li_at=AQEDAT3ooIgC4GZVAAABkAG8hcMAAAGQJckJw00AsJprgJD8JkpHZp2_KP3_MStyZJEzTfLVarHJSREX2HZPtEQ3gBKXRVp9tXcTr7UG-tXL8y5HmeeZFN136dRaTXycV9uhEgACOAwtoEP39-WlusPL; AMP_MKTG_5919ff8c0c=JTdCJTdE; sdsc=22%3A1%2C1718085518182%7EJAPP%2C08jBL0qOIZDLlXXftEwJeQ%2B9TFyI%3D; AMP_5919ff8c0c=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmM1NDJlNjM2LTkwYmItNDI0NS04NTE1LTJhN2FhZDgxMzEwYyUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4MDg3MzMxNDEzJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTcxODA4NzMzMTI5NSU3RA==; __cf_bm=JyzYqbFZ0.QQTjrJ3ROy.5uCxpIbgjMiuosgHDDn.8s-1718087685-1.0.1.1-6mTVyBHby3hUyqxwAjsltbakRigtxBrweldgOpA8PgbFCydT0xmziY35BB3Eabw2obM.SrpC5xNh9QJYs2QEDA; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19886%7CMCMID%7C42921819607459256697087020623622308298%7CMCOPTOUT-1718094980s%7CNONE%7CvVersion%7C5.1.1; UserMatchHistory=AQJV5DZ3Xor2vwAAAZAGBIfWkO02BuFZwf3VO1gFePDOWgClI-AHQ2xEm_1HTQxZjseHOa1KhsIcmGoSXicADy8NhRF6YkhUeMm-y9dKWQ2Qw9z_hFakK-YLvimM5xqHs64Xup7zqfj9kVD8ydt80YHM8TQZ_5kDtvXQERy1g9vGMyGO7Wu7LZv99v63oV9mNZ3CY_JN1qYPAYkuoJApk8LeKs-Uv6f-VottibPY-ZXpWUcFiwmHYjn9wFkzbKqfzLpL6FqC4eKUv3WlxIuLstWO_XMSBwr2YQ9nydlovSPuGVIIqoHfUI_SQdo90MTCaZlUmNhCfajH6io3G_LzP7Fb1qHZK0QAcSDXQgnIJgJ4bNdV3Q; lidc="b=VB24:s=V:r=V:a=V:p=V:g=5291:u=274:x=1:i=1718087885:t=1718171293:v=2:sig=AQHxar41hezp_F5VIBh75eDWMrJhsF_0"; _dd_s=logs=1&id=ea7b9aa7-a44d-4274-aee6-4a98b39348ef&created=1718087331004&expire=1718088780245'  # place cookie here


class LinkedIn:
    def __init__(self):
        self.fieldnames = ["Profile Link", "Name", "Designation", "Location"]

    def saveData(self, dataset):
        with open(output_file_name, mode='a+', encoding='utf-8-sig', newline='') as csvFile:

            writer = csv.DictWriter(
                csvFile, fieldnames=self.fieldnames, delimiter=',', quotechar='"')
            if os.stat(output_file_name).st_size == 0:
                writer.writeheader()
            writer.writerow({
                "Profile Link": dataset[0],
                "Name": dataset[1],
                "Designation": dataset[2],
                "Location": dataset[3]
            })

    @classmethod
    def getCompanyID(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Dnt': '1',
            'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        try:
            resp = requests.get(company_link, headers=headers).text
        except:
            print("Failed to open {}".format(company_link))
            return None
        try:
            companyID = re.findall(
                r'"objectUrn":"urn:li:organization:([\d]+)"', resp)[0]
        except:
            print("Company ID not found")
            return None
        return companyID

    def paginateResults(self, companyID):
        headers = {
            'Accept': 'application/vnd.linkedin.normalized+json+2.1',
            'Cookie': cookies,
            'Csrf-Token': re.findall(r'JSESSIONID="(.+?)"', cookies)[0],
            'Dnt': '1',
            'Referer': 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%22' + companyID + '%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page=2&sid=7Gd',
            'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'X-Li-Lang': 'en_US',
            'X-Li-Page-Instance': 'urn:li:page:d_flagship3_search_srp_people_load_more;Ux/gXNk8TtujmdQaaFmrPA==',
            'X-Li-Track': '{"clientVersion":"1.13.9792","mpVersion":"1.13.9792","osName":"web","timezoneOffset":6,"timezone":"Asia/Dhaka","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.3125,"displayWidth":1920.1875,"displayHeight":1080.1875}',
            'X-Restli-Protocol-Version': '2.0.0',
        }
        for page_no in range(0, 1000, 10):
            print("Checking facet: {}/990".format(page_no))
            link = "https://www.linkedin.com/voyager/api/graphql?variables=(start:" + str(page_no) + ",origin:COMPANY_PAGE_CANNED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List(" + \
                companyID + \
                ")),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&queryId=voyagerSearchDashClusters.e1f36c1a2618e5bb527c57bf0c7ebe9f"

            try:
                resp = s.get(link, headers=headers).json()
            except:
                print("Failed to open {}".format(link))
                continue
            results = resp.get('included')
            for person_data in results:
                if person_data.get('$type') == "com.linkedin.voyager.dash.search.EntityResultViewModel":
                    person_name = person_data.get('title').get('text')
                    profile_link = person_data.get('navigationUrl')
                    designation = person_data.get(
                        'primarySubtitle').get('text')
                    person_location = person_data.get(
                        'secondarySubtitle').get('text')
                    print("Profile Link: {}".format(profile_link))
                    print("Name: {}".format(person_name))
                    print("Designation: {}".format(designation))
                    print("Location: {}".format(person_location))
                    print()
                    dataset = [profile_link, person_name,
                               designation, person_location]
                    self.saveData(dataset)
            print("Waiting for {} seconds".format(pagination_delay))
            sleep(pagination_delay)


if __name__ == "__main__":
    companyID = LinkedIn.getCompanyID()
    if companyID is not None:
        linkedin = LinkedIn()
        linkedin.paginateResults(companyID)