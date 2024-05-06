cd package
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip lambda_function.py
zip my_deployment_package.zip linkedin_database.db