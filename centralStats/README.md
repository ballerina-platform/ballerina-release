<!-- STEPS TO USE YOUR OWN SPREADSHEET -->

Configurations
    Config.toml -   
        Refer this -  https://ei.docs.wso2.com/en/7.0.0/micro-integrator/references/connectors/google-spreadsheet-connector/get-credentials-for-google-spreadsheet/

        spreadsheetClientID = //YOUR GOOGLE SHEETS CLIENT ID
        spreadsheetClientSecret = //YOUR GOOGLE SHEETS CLIENT SECRET
        spreadsheetRefreshToken = //YOUR GOOGLE SHEETS REFRESH TOKEN
        spreadsheetID = Get your specific spreadsheet's ID 
                        You can get it from its url - https://docs.google.com/spreadsheets/d/<spreadsheetID>/edit#gid=xxxxxxxxx

        Search foe the content with "// UNCOMMENT THIS FOR INITIAL CONFIGURATIONS ONLY" this comment 
        Next uncommnet those and do bal run

            