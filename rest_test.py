'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Mar 06 2024
File : registration.py
'''
import sys, os, json, requests

###################################################################################
# Test the version of python to make sure it's at least the version the script
# was tested on, otherwise there could be unexpected results
if sys.version_info < (3, 6):
    raise Exception("The current version of Python is less than 3.6 which is unsupported.\n Script created/tested against python version 3.10.1. ")
else:
    pass

propertiesFile = "../server_properties.json"  # Created by installer or manually
defaultBaseURL = "DEFAULT_VALUE" # i.e. http://localhost:8888 or https://sca.mycodeinsight.com:8443 
defaultAdminAuthToken = "DEFAULT_VALUE"
defaultCertificatePath = "DEFAULT_VALUE"

#----------------------------------------------------------------------#
def main():

    print("")

    if os.path.exists(propertiesFile):
        print("Properties file exists: %s" %propertiesFile)
        try:
            file_ptr = open(propertiesFile, "r")
        except:
            print("Unable to open properties file: %s" %propertiesFile)
        else:
            print("Opened properties file: %s" %propertiesFile)
            configData = json.load(file_ptr)
            file_ptr.close()
            print("")
            print("configData:  %s" %configData)

            # The file exists so can we get the config data from it?
            if "core.server.url" in configData:
                print("    baseURL pulled from configData")
                baseURL = configData["core.server.url"]
            else:
                print("    core.server.url not in configData using default value")
                baseURL = defaultBaseURL
            
            if "core.server.token" in configData:
                print("    adminAuthToken pulled from configData")
                adminAuthToken = configData["core.server.token"]
            else:
                print("    core.server.token not in configData using default value")
                adminAuthToken = defaultAdminAuthToken 
            
            if "core.server.certificate" in configData:
                print("    certificatePath pulled from configData")
                certificatePath = configData["core.server.certificate"]
            else:
                print("    core.server.certificate not in configData using default value")
                certificatePath = defaultCertificatePath
    else:
        print("Properties file does not exist: %s" %propertiesFile)
        print("Using config data from registration.py")
        baseURL = defaultBaseURL
        adminAuthToken = defaultAdminAuthToken
        certificatePath = defaultCertificatePath

    print("")
    print("Values:")
    print("    baseURL: %s" %baseURL)
    print("    adminAuthToken: %s" %adminAuthToken)
    print("    certificatePath: %s" %certificatePath)
    print("")
        

    if certificatePath != "DEFAULT_VALUE":
        if os.path.exists(certificatePath):
            print("%s file exists" %certificatePath)
            os.environ["REQUESTS_CA_BUNDLE"] = certificatePath
            os.environ["SSL_CERT_FILE"] = certificatePath
            print("Cert environment variables set")
        else:
            print("%s file does not exist" %certificatePath)
    else:
        print("Cert env variables not updated since path not provided")
       

    if "DEFAULT_VALUE" in [baseURL, adminAuthToken]:
        print("")
        print("Defalut values are required for both baseURL and adminAuthToken")
        print(" ** Exiting ** ")
        sys.exit()
    else:
        print("")
        print("Get Code Insight release Details")
        releaseDetails = get_release_details(baseURL, adminAuthToken)

        print("    %s" %releaseDetails)
	

#----------------------------------------------------
def get_release_details(baseURL, authToken):

    RESTAPI_BASEURL = "%s/codeinsight/api" %(baseURL)
    RESTAPI_URL = "%s/v1/agent/supports" %(RESTAPI_BASEURL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        return {"error" : error}

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        releaseDetails = json.loads(response.json()["Content: "])
        return releaseDetails
    else:
        return {"error" : response.text}


#----------------------------------------------------------------------#    
if __name__ == "__main__":
    main()    
