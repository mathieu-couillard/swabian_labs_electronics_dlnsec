import pyvisa as visa


class DLnSec:
    def __init__(self, addr, verbatim=False):
        # You may have to run this command "sudo chmod 666 /dev/ttyUSB0"
        # Or "sudo usermod -a -G dialout <unsername>"
        self._inst = visa.ResourceManager('@py').open_resource(addr)
        self._inst.read_termination = '\n\r'
        self._inst.timeout = 5e3
        self._verbatim = verbatim

    ##############################
    # Basic commands
    ##############################

    def identify(self):
        return self._com('*IDN?')

    def idn(self):
        return self.identify()

    def save(self):
        return self._com('*SAV')

    def recall(self):
        return self._com('*RCL')

    def n_saved(self):
        # Number of saved settings
        return self._com('NSAV?')

    def howdy(self):
        return self._com('HOWDY?')

    def restart(self):
        return self._com('*RST')

    def error(self):
        return self._com("ERR?")

    def output_on(self):
        return self._com("*ON")

    def output_off(self):
        return self._com("*OFF")

    def cw(self):
        return self._com("LAS")

    def continuous_wave(self):
        return self.cw()

    def trig_internal(self):
        return self._com("INT")

    def trig_external(self):
        return self._com("EXT")

    def stop_laser(self):
        return self._com("STOP")

    def power(self, percentage='?'):
        if percentage > 0 or percentage < 100 or percentage == '?':
            return self._com("PWR{}".format(percentage))
        else:
            Exception('InvalidPowerLevelException: Value must be between 0 and 100')

    def pow(self, percentage='?'):
        return self.power(percentage)

    def prescaler(self, prescale='?'):
        options = [1, 8, 64, 256, 1024, '?']
        if prescale in options:
            return self._com("PRE{}".format(prescale))
        else:
            Exception('InvalidInternalTriggerFrequencyDivider: Valid repetition rates are 16MHz/256/P' +
                      'Where P is one of the valid inputs: {}'.format(prescale))

    def pulse_width(self, width='?'):
        if 0 <= width <= 255 or width == '?':
            return self._com("PRE{}".format(width))
        else:
            Exception('InvalidPulseWidthMultiplier: Valid pulse widths are 1/16MHz*<P>*<N+1>' +
                      'Where N is one of the valid inputs: {} and P is the prescaler value '.format(width) +
                      'for the repetition rate.')

    ##############################
    # User friendly commands
    ##############################
    def trigger(self, trig_type):
        options = {'int': self.trig_internal,
                   'internal': self.trig_internal,
                   'ext': self.trig_external,
                   'external': self.trig_external,
                   'cw': self.continuous_wave(),
                   'continuous':self.continuous_wave()}
        try:
            options[trig_type]()
        except KeyError:
            print('Valid keys are: {}'.format(options.keys()))

    def quick_cw(self, power):
        self.continuous_wave()
        self.power(power)
        self.output_on()

    def quick_start(self, power, trig='', prescale=1024, pulse_width=255):
        options = ['int', 'internal', 'ext', 'external', 'wc', 'continuous']
        if trig in options:
            if options == 'int' or options == 'internal':
                # TODO: Test this
                self.set_parameters(prescale=prescale, pulse_width=pulse_width)
                # self.trig_internal()
                # self.prescaler(prescale)
                # self.pulse_width(pulse_width)
            if options == 'ext' or options == 'external':
                self.trig_external()
            if options == 'cw' or options == 'continuous':
                self.continuous_wave()
        else:
            Exception('InvalidTriggerException. Valid options are {}'.format(options))
        self.power(power)
        self.output_on()

    def get_parameters(self):
        # TODO: return all parameters as a list
        param = {'power': self.power(),
                 'prescale': self.prescaler(),
                 'pulse_width': self.pulse_width()
                 }
        return param

    def set_parameters(self, **kwargs):
        commands = {'power': self.power,
                    'prescale': self.prescaler,
                    'pulse_width': self.pulse_width
                    }

        for k in kwargs.keys():
            try:
                commands[k](kwargs[k])
            except KeyError:
                pass

    ##############################
    # send commands
    ##############################
    def _com(self, cmd):
        if self._verbatim:
            print(cmd)
        if cmd[-1] == '?':
            # The manufacturer did not follow the proper SCPI standard
            if cmd == "*IDN?" or "HOWDY?":
                cmd = cmd[:-1]
            value = self._inst.query(cmd)
            try:
                return float(value)
            except:
                return value
        else:
            self._inst.write(cmd)
            return "Sent: " + cmd


if __name__ == "__main__":
    laser = DLnSec('ASRL/dev/ttyUSB0::INSTR', verbatim=True)
    print(laser.identify())
    print(laser.error())
    print(laser.power())
