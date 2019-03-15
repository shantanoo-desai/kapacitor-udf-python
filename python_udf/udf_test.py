from kapacitor.udf.agent import Agent, Handler
from kapacitor.udf import udf_pb2
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()


class HashHandler(Handler):
    def __init__(self, agent):
        logger.info('__init__ trigger')
        self._agent = agent
        self._field = ' '
        self._size = 20
        self._points = []
        self._state = {}

    def info(self):
        logger.info('info trigger')
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.BATCH
        response.info.provides = udf_pb2.STREAM
        response.info.options['field'].valueTypes.append(udf_pb2.STRING)
        return response

    def init(self, init_req):
        logger.info('INIT trigger')
        for opt in init_req.options:
            if opt.name == 'field':
                self._field = opt.values[0].stringValue
        success = True
        msg = ''
        if self._field == '':
            success = False
            msg = 'must provide field name'
        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg.encode()
        return response

    def begin_batch(self, begin_req):
        logger.info('begin_batch trigger')


    def point(self, point):
        logger.info('point trigger')
        self._points.append(point.fieldsDouble[self._field])
        if len(self._points) == self._size:
            geo = 1.0
            for p in self._points:
                logger.debug('loop' + str(p))
                geo *= p
            logger.debug(str(geo))
            response = udf_pb2.Response()
            response.point.name = point.name
            response.point.time = point.time
            response.point.group = point.group
            response.point.tags.update(point.tags)
            response.point.fieldsDouble['geo'] = geo
            response.point.fieldsString['hash'] = 'test'
            self._agent.write_response(response)
            self._points.pop(0)

    def end_batch(self, batch_meta):
        logger.info('end_batch')



if __name__ == '__main__':
    # Create an agent
    agent = Agent()

    # Create a handler and pass it an agent so it can write points
    h = HashHandler(agent)

    # Set the handler on the agent
    agent.handler = h

    # anything printed to STDERR from a UDF process gets captured into the logs
    logger.info("Starting agent for HashHandler")
    agent.start()
    agent.wait()
    logger.info("Agent finished")

