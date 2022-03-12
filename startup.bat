C:\ngrok\ngrok.exe http --region=us --hostname=usda-data-receiving.ngrok.io 5000 &

source ./env/Scripts/activate &

python src/gps_webhook_listener_flask.py >> C:\range_project_new\logs\gps_webhook_listener_flask.log &
python statistics/MCP/MCPCalculation.py >> C:\range_project_new\logs\MCPCalculation.log &
python statistics/record_count.py >> C:\range_project_new\logs\record_count.log &
