#!/use/bin/env python
# -*- coding:utf-8 -*_


class IOProt:

    def __init__(self, transport):
        self._trans = transport
        self._body = {}
        self._message = []
        self._phase = 0
        self._res_data = []
        self._args_num = 0

    @property
    def trans(self):
        return self._trans

    def write_begin(self, method_name=''):
        self._message = []
        if method_name:
            self._message.append('0%02d%s' % (len(method_name), method_name))
        else:
            self._message.append('1')

    def write_int(self, int_value):
        value = str(int_value)
        self._message.append('0%02d%s' % (len(value), value))

    def write_string(self, str_value):
        self._message.append('1%04d%s' % (len(str_value), str_value))

    def write_end(self):
        args_num = len(self._message) - 1
        self._message.insert(1, '%02d' % args_num)
        self._flush()

    def bye(self):
        self._message = ['2']
        self._flush()
        self._trans.close()

    def _flush(self):
        self._trans.write(''.join(self._message))

    def read_body(self):
        self._body = {}
        self._phase = 0
        for data in self._trans.read(1024):
            if not data or self._parse(data):
                break
        return self._body

    def _parse(self, data):
        if data[0] == '2':
            self._body['close'] = True
            return True
        if self._phase == 0:
            data = self._read_begin(data)
        return self._read_params(data)

    def _read_begin(self, data):
        self._body['call_type'] = data[0]
        if data[0] == '0':
            m_length = int(data[1:3])
            self._body['method_name_length'] = m_length
            self._body['method_name'] = data[3:3+m_length]
            data = data[3+m_length:]
        else:
            self._body['method_name_length'] = 0
            self._body['method_name'] = ''
            data = data[1:]
        self._args_num = int(data[:2])
        self._phase = 1
        return data[2:]

    def _read_params(self, data):
        if self._res_data:
            data = self._res_data + data
        for i in range(0, self._args_num):
            if len(data) == 0:
                return False
            if data[0] == '0':
                l, err = self._read_int(data)
            else:
                l, err = self._read_string(data)
            if err:
                self._res_data = data
                return False
            data = data[l:]
        return True

    def _read_int(self, data):
        if len(data) < 4:
            return 0, True
        l = int(data[1:3])
        if len(data) < l + 3:
            return 0, True
        self._body.setdefault('args', [])
        self._body['args'].append(int(data[3:3+l]))
        return 3 + l, False

    def _read_string(self, data):
        if len(data) < 6:
            return 0, True
        l = int(data[1:5])
        if len(data) < 1 + 5:
            return 0, True
        self._body.setdefault('args', [])
        self._body['args'].append(data[5:5+l])
        return 5 + l, False
