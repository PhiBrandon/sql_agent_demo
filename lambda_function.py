from langchain_community.utilities import SQLDatabase
import os
import shutil

db = SQLDatabase.from_uri("sqlite:///linkedin_database.db")
db.run("""SELECT p.profile_name, e.company, e.title FROM experiences e JOIN profiles p ON e.profile_id = p.profile_id WHERE p.profile_name LIKE 'Brandon%'""")


def get_tables():
    tables = db.get_usable_table_names()
    return tables


def get_tables_information(t: list[str]):
    res = eval(t)
    return db.get_table_info(res)


def lambda_handler(event, context):
    original_db_file = "linkedin_database.db"
    target_db_file = "/tmp/linkedin_database.db"
    if not os.path.exists(target_db_file):
        shutil.copy2(original_db_file, target_db_file)

    agent = event["agent"]
    actionGroup = event["actionGroup"]
    function = event["function"]
    parameters = event.get("parameters", [])
    responseBody = {"TEXT": {"body": "Error, no function was called"}}
    if function == "get_tables":
        tables = get_tables()
        responseBody = {"TEXT": {"body": f"<tables_list>{tables}</tables_list>"}}
    elif function == "get_tables_information":
        tables = None
        for param in parameters:
            if param["name"] == "tables_list":
                tables = param["value"]
        if not tables:
            raise Exception("Missing mandatory parameter: tables_list")
        print(tables)
        table_information = get_tables_information(tables)
        responseBody = {
            "TEXT": {
                "body": f"<tables_information>{table_information}</tables_information>"
            }
        }
    action_response = {
        "actionGroup": actionGroup,
        "function": function,
        "functionResponse": {"responseBody": responseBody},
    }

    function_response = {
        "response": action_response,
        "messageVersion": event["messageVersion"],
    }
    print("Response: {}".format(function_response))

    return function_response