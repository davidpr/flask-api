from app import create_app
import os 
import sys

settings_module = os.getenv('APP_SETTINGS_MODULE')

print  ('APP_SETTINGS_MODULE: ->> '+str(os.getenv('APP_SETTINGS_MODULE')),  file=sys.stderr)

app = create_app(settings_module)


# print ('entering by routes.py\n',  file=sys.stderr)
# port = int(os.environ.get('PORT', 4444))
# app.run(debug=True, host='0.0.0.0', port=port)


if __name__ == '__main__':
    print ('entering by entrypoint.py\n',  file=sys.stderr)
    port = int(os.environ.get('PORT', 4444))
    app.run(debug=True, host='0.0.0.0', port=port)
else: 
    print ('entering by other side.',  file=sys.stderr)
    