import argparse
import requests
import json

class graphql:

    current_bearer_token = None
    args = None
    verbose = True

    def __init__(self, authenticator, password, username, role, endpoint, verbose):
        self.parser = None

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-a", "--authenticator", type=str, default=authenticator)
        self.parser.add_argument("-p", "--password", type=str, default=password)
        self.parser.add_argument("-n", "--name", type=str, default=username)
        self.parser.add_argument("-r", "--role", type=str, default=role)
        self.parser.add_argument("-u", "--url", type=str, default=endpoint)
        graphql.args = self.parser.parse_args()
        graphql.verbose = verbose

    def post(self, content):
        if graphql.current_bearer_token == None:
            graphql.current_bearer_token = self.get_bearer_token(self)
        try:
            response = self.perform_graphql_request(self, content)
        except requests.exceptions.HTTPError as e:
            if "forbidden" in str(e).lower() or "unauthorized" in str(e).lower():
                if graphql.verbose == True:
                    print ("Not authorized, getting new token...")
                graphql.current_bearer_token = self.get_bearer_token(self)
                response = self.perform_graphql_request(self, content)
            else:
                print("An unhandled error occured accessing the SM Platform!")
                print(e)
                raise requests.exceptions.HTTPError(e)
        return response

    def perform_graphql_request(self, content, auth=False):
        if graphql.verbose == True:
            print("Performing request with content: ")
            print(content)
            print()
        if auth == True:
            header=None
        else:
            header={"Authorization": graphql.current_bearer_token}
        r = requests.post(graphql.args.url, headers=header, data={"query": content})
        r.raise_for_status()
        return r.json()
        
    def get_bearer_token (self):
        response = self.perform_graphql_request(self, f"""
        mutation authRequest {{
                authenticationRequest(
                    input: {{authenticator: "{graphql.args.authenticator}", role: "{graphql.args.role}", userName: "{graphql.args.name}"}}
                ) {{
                    jwtRequest {{
                    challenge, message
                    }}
                }}
                }}
            """, True) 
        jwt_request = response['data']['authenticationRequest']['jwtRequest']
        if graphql.verbose == True:
            print ("got auth request response")
        if jwt_request['challenge'] is None:
            print ("no challenge in response")
            raise requests.exceptions.HTTPError(jwt_request['message'])
        else:
            if graphql.verbose == True:
                print("Challenge received: " + jwt_request['challenge'])
            response=self.perform_graphql_request(self, f"""
                mutation authValidation {{
                authenticationValidation(
                    input: {{authenticator: "{graphql.args.authenticator}", signedChallenge: "{jwt_request["challenge"]}|{graphql.args.password}"}}
                    ) {{
                    jwtClaim
                }}
                }}
            """, True)
        jwt_claim = response['data']['authenticationValidation']['jwtClaim']
        return f"Bearer {jwt_claim}"

    def build_alias_ts_mutation(self, timestamp, ordinal, attributeOrTagId, value):
        smp_mutation = f'''ts{ordinal}: replaceTimeSeriesRange (
                                input: {{
                                        entries: [
                                                {{ status: "0", timestamp: "{timestamp}", value: "{value}" }}
                                        ]
                                        attributeOrTagId: "{attributeOrTagId}"
                                }}) {{
                                        json
                                }}
                                '''
        return smp_mutation

    def multi_tsmutate_aliases(self, aliasmutations):
            smp_mutation = f'''mutation tsmulti {{
                                    {aliasmutations}
                            }}
                            '''		
            smp_response = ""
            try:
                    smp_response = self.post(self, smp_mutation)
                    if 'errors' in smp_response:
                            print("\033[31mThe SM Platform returned an error during a write operation:\033[0m")
                            print(smp_response['errors'])
                    return smp_response
            except requests.exceptions.HTTPError as e:
                    print("\033[31mAn error occured writing to the SM Platform:\033[0m")
                    print(e)