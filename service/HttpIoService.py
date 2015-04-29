#!flask/bin/python
import time, os
import json
from json import *
from flask import Flask, request, jsonify, render_template
from config import serverConfig
from loInterpreter import TiloInterpreter
from ConsoleInterpreter import TxConsoleInterpreter

class TxHttpIoService(TiloInterpreter):
    server = Flask('HttpIoService')
    consoles = TxConsoleInterpreter()

    def __init__(self, inputConfig = {}):
        self.config = inputConfig
        self.server.debug = inputConfig['debug']

    def startup(self):
        self.server.run(host = self.config['host'], port = self.config['port'])

    @server.route('/service', methods = ['GET'])
    def service():
        command = request.args.get('command', 'null')
        appService = TxHttpIoService.appService

        if command == 'restart':
            appService.restart()

        if command == 'shutdown':
            appService.shutdown()

        return jsonify(command=command)

    @server.route('/scheduler', methods = ['GET'])
    def scheduler():
        appService = TxHttpIoService.appService

        # return jsonify({'tasks': 1, 'running': 1})
        if appService.scheduler:
            return json.dumps(appService.scheduler.__dict__)

    @server.route('/scheduler/running', methods = ['GET','POST'])
    def schedulerRunning():
        appService = TxHttpIoService.appService

        if request.method == 'GET':
            running = appService.scheduler.running
            if running:
                rt=running.to_dict()
            else:
                rt=None
            return json.dumps(rt)

        elif request.method == 'POST':
            req_data=request.get_json()
            appService.interprete(req_data,-1)
            return json.dumps(req_data)

    @server.route('/scheduler/waiting', methods = ['GET', 'POST'])
    def schedulerWaiting():
        appService = TxHttpIoService.appService

        if request.method == 'GET':
            return json.dumps(appService.scheduler.getWaitingList())

    @server.route('/tasks', methods = ['GET', 'POST'])
    def tasks():
        appService = TxHttpIoService.appService

        if request.method == 'GET':
            flows=appService.scheduler.getAllFlows()
            #return jsonify(result=flows)
            return json.dumps(flows)

        elif request.method == 'POST':
            #req_data=request.form.to_dict()
            req_data=request.get_json()

            if req_data and req_data.has_key('immediate') and req_data['immediate']=='true':
                appService.interprete(req_data,-1)

            else:
                appService.interprete(req_data)

            return json.dumps(req_data)

    @server.route('/tasks/<int:flow_id>', methods=['GET','DELETE'])
    def taskId(flow_id):
        appService = TxHttpIoService.appService

        if request.method == 'GET':
            rt=appService.scheduler.getFlowById(flow_id)
            return json.dumps(rt)

        elif request.method == 'DELETE':
            req_data=request.args.get('force','false')
            force=False

            if req_data == 'true':
                force=True

            if appService.scheduler.flows.flows.has_key(str(flow_id)):
                rt=appService.scheduler.flows.flows.pop(str(flow_id)).to_dict()
                que=(appService.scheduler.getWaitingList())

                for i in range(len(que)):
                    print 'queue index=',i
                    if que[i].id==flow_id:
                        que.pop(i)

                if force == True and appService.scheduler.running:
                    if appService.scheduler.running.id == flow_id:
                        appService.scheduler.kill_running()

            else:
                rt=None

            return json.dumps(rt)

    @server.route('/tasks/<int:flow_id>/input')
    def taskIdInput(flow_id):
        appService = TxHttpIoService.appService
        flow = appService.scheduler.getFlowById(flow_id)
        return jsonify(result = (flow and flow.get('inputs') or []))

    @server.route('/tasks/<int:flow_id>/output')
    def taskIdOutput(flow_id):
        appService = TxHttpIoService.appService
        flow = appService.scheduler.getFlowById(flow_id)
        return jsonify(result = (flow and flow.get('outputs') or []))

    @server.route('/test')
    def test():
        try:
            appService = TxHttpIoService.appService

        except Exception as e:
            print e

        return render_template('test.html', scheduler=appService.scheduler)

    @server.route('/myconsole',methods=['POST','GET'])
    def myconsole():
        if not TxHttpIoService.consoles.is_started():
            TxHttpIoService.consoles.start()

        uuid = request.args.get('uuid')
        ctrl = request.args.get('ctrl')
        cmd = request.data
        print 'uuid=%s,cmd=%s'%(uuid,cmd)

        if ctrl == 'terminate':
            TxHttpIoServer.consoles.input_cmd(uuid,'clear')

        TxHttpIoService.consoles.input_cmd(uuid,cmd)
        return jsonify(result=1)

    @server.route('/lsjtest')
    def lsjtest():
        cmd = request.args.get('cmd')

        return jsonify(result=1)

    # @server.route('/jquery.min.js')
    # def jquery():
    #     appService = TxHttpIoService.appService
    #     return render_template('jquery.min.js', scheduler=appService.scheduler)
