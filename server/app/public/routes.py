from flask import request, render_template
from . import public_bp
import logging


import os
import uuid
import json
import sys
import pathlib

from app.scheduler import Scheduler
from app.atomic_ops_scheduler import Atomic_ops_scheduler
from app.searcher import Searcher

from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage



scheduler = Scheduler()
atopmic_ops_scheduler = Atomic_ops_scheduler()
searcher = Searcher()

env = load_dotenv()
       
logging.basicConfig(stream=sys.stderr,level=logging.os.getenv('PRINT_MODE'))


@public_bp.route("/")
def home():
    return f'OK'


@public_bp.route('/sum')
def sum():
    string1 = 'result_sum'
    return f'sum is: {string1}'


@public_bp.route('/test')
def test():
    return f'Test OK'


@public_bp.route('/deploy', methods=['POST', 'GET'])
def deploy():

    f = request.files['file1']
    f.save(secure_filename(f.filename))


    # help disploy
    if "h" in request.form:
        #  logging.debug('Usage:\n' \
        #  +'-r: ram'\
        #  )
        # return
        return f'Usage:\n' \
            + '-r: ram'

    # -gather and save the inputs. Some are mandatory, some optional with defaults
    # -parameters are better sent without '-' character as it is problematic then when
    # doing some manipulations
    input_ram = request.form['r']
    input_workload = request.form['w']
    input_runtime = request.form['rt']
    input_cores = "1"
    input_provider = "agnostic"

    # cores
    if "c" in request.form:
        input_cores = request.form['c']
        logging.debug('c exists\n')
    else:
        logging.debug('c does not exist\n')
    # providers
    if "p" in request.form:
        input_provider = request.form['p']
        logging.debug('p exists\n')
    else:
        logging.debug('p does not exist\n')

    # uuid for each petition
    id_petition = uuid.uuid4()

    path_file = str(pathlib.Path(__file__).parent.resolve()) + \
        '/../../workloads/dbFile.json'
    logging.debug(path_file)

    json_string = {
        "_id": str(id_petition),
        "provider": str(input_provider),
        "cores": int(input_cores),
        "ram": int(input_ram),
        "runtime": str(input_runtime),
        "workload": str(input_workload)
    }

    if not os.path.exists(path_file) or os.stat(path_file).st_size == 0:
        with open(path_file, 'a') as db_file:
            db_file.write('[\n')
            json.dump(json_string, db_file, indent=4)
            db_file.write('\n')
            db_file.write(']\n')

        db_file.close()
    else:
        with open(path_file, 'r+') as db_file:
            lines = db_file.readlines()
            db_file.seek(0)
            db_file.truncate()
            for number, line in enumerate(lines):
                if number != len(lines)-1:
                    db_file.write(line)
                else:
                    db_file.write(',\n')

            json.dump(json_string, db_file, indent=4)
            db_file.write('\n')
            db_file.write(']\n')

        db_file.close()

    #res = scheduler.schedule(id_petition, input_ram, input_workload, input_runtime, input_cores, input_provider )
    res = atopmic_ops_scheduler.schedule(
        id_petition, input_ram, input_workload, input_runtime, input_cores, input_provider)

    # return an html with the results of the operation
    return render_template('result.html', pred=f'CLI petition was: am deploy -r {input_ram} -w {input_workload} -rt {input_runtime} -c {input_cores} -p {input_provider}. Petition UUID: {id_petition}\n')

@public_bp.route('/list')
def list():
    res = searcher.retrieveWorkloads()

    return res

@public_bp.route('/remove', methods=['POST', 'GET'])
def remove():
    input_id_petition = request.form['id_p']
    res = atopmic_ops_scheduler.end_workload(input_id_petition)

    return 'hi'#str(res)

