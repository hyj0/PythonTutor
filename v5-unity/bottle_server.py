# Lightweight OPT server that works on both Python 2 and 3

# NOTE that this is meant only for testing and not deployment, since
# there is no sandboxing

# to invoke, run 'python bottle_server.py'
# and visit http://localhost:8080/index.html
#
# external dependencies: bottle
#
# easy_install pip
# pip install bottle
import os
import sys

from bottle import route, get, request, run, template, static_file, response
try:
    import StringIO # NB: don't use cStringIO since it doesn't support unicode!!!
except:
    import io as StringIO # py3
import json
import pg_logger


@route('/web_exec_<name:re:.+>.py')
@route('/LIVE_exec_<name:re:.+>.py')
@route('/viz_interaction.py')
@route('/syntax_err_survey.py')
@route('/runtime_err_survey.py')
@route('/eureka_survey.py')
@route('/error_log.py')
def dummy_ok(name=None):
    return 'OK'

@route('/<filepath:path>')
def index(filepath):
    return static_file(filepath, root='.')


# Note that this will run either Python 2 or 3, depending on which
# version of Python you used to start the server, REGARDLESS of which
# route was taken:
@route('/web_exec_py2.py')
@route('/web_exec_py3.py')
@route('/LIVE_exec_py2.py')
@route('/LIVE_exec_py3.py')
def get_py_exec():
  if True:
      path = os.path.join(os.path.split(__file__)[0], "..")
      path = os.path.join(path, '..')
      path = os.path.join(path, 'python_out.json')
      f = open(path, 'r')
      s = f.read()
      f.close()
      return s

  out_s = StringIO.StringIO()

  def json_finalizer(input_code, output_trace):
    ret = dict(code=input_code, trace=output_trace)
    json_output = json.dumps(ret, indent=None)
    out_s.write(json_output)

  options = json.loads(request.query.options_json)

  pg_logger.exec_script_str_local(request.query.user_script,
                                  request.query.raw_input_json,
                                  options['cumulative_mode'],
                                  options['heap_primitives'],
                                  json_finalizer)

  return out_s.getvalue()

@route('/exec_c_jsonp')
@route('/exec_cpp_jsonp')
def exec_c_jsonp():
    path = os.path.join(os.path.split(__file__)[0], "..")
    path = os.path.join(path, '..')
    path = os.path.join(path, 'cpp_out.json')
    f = open(path, 'r')
    s = f.read()
    f.close()

    response.headers['Content-Type'] = 'text/javascript; charset=utf-8'

    retStr = s
    retStr = "/*414*/\ntypeof %s === 'function' && %s(" %(request.GET.dict['callback'][0], request.GET.dict['callback'][0])  + retStr + ");"
    return retStr

def exec_c_jsonp1():
    if True:
        path = os.path.join(os.path.split(__file__)[0], "..")
        path = os.path.join(path, '..')
        path = os.path.join(path, 'cpp_out.json')
        f = open(path, 'r')
        s = f.read()
        f.close()
        return s

if __name__ == "__main__":
    run(host='0.0.0.0', port=8003, reloader=True)
