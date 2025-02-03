from testProxy import test_proxy
import requests

def postScraper(url, data):

    import requests
    import re
    from bs4 import BeautifulSoup

    headers = {
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        "entities":"eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3MzgxNDg4MTYsImlzcyI6ImV2ZW50LWNsb3VkLmNvbSIsInN1YiI6IjcxMTM2MTEiLCJ0eXBlIjoiYmVDb25uZWN0aW9uIn0.QiK2SNct4fPcFIwmuWvvLcnrHVO_F47ctvhbkFqtHrtPumRE6dnyhVH3TpoJx7YfDCnlfWsxPJ5uu1KlxEsxHA",
        "dnt":"1",
        "ec-client":"EventGuide/2.12.1-9381[52]",
        "ec-client-branding":"2023_itb",
        "origin":"https://navigate.itb.com"
    }


    response = requests.post(url, headers=headers, data=data)
    print(response)

    if response.status_code == 200:
        #print(response.text)
        s = BeautifulSoup(response.text, "xml")

        exportData = []
        
        items = s.find_all("organization")
        print("ITEMS length:  " + str(len(items)))

        for i in items:
            NAME = i.get("name")
            COUNTRY = i.get("country")
            CITY = i.get("city")
            POSTALCODE = i.get("postCode")
            contacts = i.find("contacts")

            if contacts:
                contactsPerson = contacts.find("contactPerson")
                if contactsPerson:
                    CONTACT_NAME = contactsPerson.get("firstName") + " " +contactsPerson.get("lastName")
                    CONTACT_NAME_POSITION = contactsPerson.get("position")
                else:
                    CONTACT_NAME = ""
                    CONTACT_NAME_POSITION = ""
            else:
                CONTACT_NAME = ""
                CONTACT_NAME_POSITION = ""

            idForWebsite = i.get("id")
            nameForWebsite = i.get("name")
            if not nameForWebsite[-1].isalpha():
                nameForWebsite = nameForWebsite[:-1]
            
            nameForWebsite = nameForWebsite.replace("™", "-tm-")
            nameForWebsite = nameForWebsite.replace("™ ", "-tm-")
            nameForWebsite = nameForWebsite.replace(" – ", "-")
            nameForWebsite = nameForWebsite.replace(" & ", "&")
            nameForWebsite = re.sub(r"[–&.,()™]", "-", nameForWebsite)
            nameForWebsite = re.sub(r"\s+", "-", nameForWebsite)
            nameForWebsite = re.sub(r"-{2,}", "-", nameForWebsite)
    
    
            WEBSITE = "https://navigate.itb.com/company/" + nameForWebsite.strip("-") + "--" + idForWebsite

            exportData.append ({
                "NAME": NAME,
                "COUNTRY": COUNTRY,
                "CITY": CITY,
                "POSTALCODE": POSTALCODE,
                "WEBSITE": WEBSITE,
                "CONTACT_NAME": CONTACT_NAME,
                "POSITION": CONTACT_NAME_POSITION
            })
        
        return exportData


    else:
        print("Error HTTP: "+ str(response.status_code))