# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget


import pysoem
import time
import ctypes
tmcm1617 = None
open_flag = 0
master = pysoem.Master()


class InputPdo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('modes_of_operation_display', ctypes.c_int8),
        ('statusword', ctypes.c_uint16),
        ('position_demand_value', ctypes.c_int32),
        ('position_actual_value', ctypes.c_int32),
        ('velocity_demand_value', ctypes.c_int32),
        ('velocity_actual_value', ctypes.c_int32),
        ('torque_demand_value', ctypes.c_int32),
        ('torque_actual_value', ctypes.c_int32),
        ('digital_input', ctypes.c_uint32),
    ]


class OutputPdo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('modes_of_operation', ctypes.c_int8),
        ('controlword', ctypes.c_uint16),
        ('target_position', ctypes.c_int32),
        ('target_velocity', ctypes.c_int32),
        ('target_torque', ctypes.c_int32),
        ('digital_output', ctypes.c_uint32),
    ]


modes_of_operation = {
    'No mode': 0,
    'Profile position mode': 1,
    'Profile velocity mode': 3,
    'Homing mode': 6,
    'Cyclic synchronous position mode': 8,
    'Cyclic synchronous velocity mode': 9,
    'Cyclic synchronous torque mode': 10,
}

def convert_input_data(data):
    return InputPdo.from_buffer_copy(data)


def tmcm1617_config_func(slave_pos):
    global tmcm1617
    # limit maximum current
    tmcm1617.sdo_write(0x2003, 0, (2000).to_bytes(length=4, byteorder='little', signed=False))
    # set torque control P value
    tmcm1617.sdo_write(0x2041, 1, (50).to_bytes(length=2, byteorder='little', signed=False))
    # set torque control I value
    tmcm1617.sdo_write(0x2041, 2, (20).to_bytes(length=2, byteorder='little', signed=False))
    # set motor type = BLDC
    tmcm1617.sdo_write(0x2050, 0, bytes([3]))
    # set commutation mode = Hall sensors
    tmcm1617.sdo_write(0x2055, 0, bytes([2]))
    # inverse hall direction
    tmcm1617.sdo_write(0x2070, 2, bytes([1]))
    # tune hall PHI_E offset
    tmcm1617.sdo_write(0x2070, 4, (10500).to_bytes(length=2, byteorder='little', signed=True))



class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.SearchB.clicked.connect(self.Serch)
        self.ui.CloseB.clicked.connect(self.Close)
        self.ui.OpenB.clicked.connect(self.Open)

    def Serch(self):
        #master = pysoem.Master()
        for nic in pysoem.find_adapters():
            print(nic)
            self.ui.textE.appendPlainText(nic.name)

    def Close(self):
        self.close()


    def Open(self):
        #master = pysoem.Master()
        try:
            master.open(self.ui.masterLE.text())
            if master.config_init() > 0:
                print('Master is opened')
                self.open_flag = 1
            else:
                print('no device found')
            master.close()
        except:
            print('Invalid Master adress')

    def Move(self):
        if self.open_flag == 1:
            tmcm1617 = master.slaves[0]
            tmcm1617.config_func = tmcm1617_config_func
            master.config_map()
            if master.state_check(pysoem.SAFEOP_STATE, 50_000) == pysoem.SAFEOP_STATE:
                master.state = pysoem.OP_STATE
                master.write_state()
                master.state_check(pysoem.OP_STATE, 5_000_000)
                if master.state == pysoem.OP_STATE:
                    output_data = OutputPdo()
                    output_data.modes_of_operation = modes_of_operation['Profile velocity mode']
                    output_data.target_velocity = 500  # RPM
                    for control_cmd in [6, 7, 15]:
                        output_data.controlword = control_cmd
                        tmcm1617.output = bytes(output_data)  # that is the actual change of the PDO output data
                        master.send_processdata()
                        master.receive_processdata(1_000)
                        time.sleep(0.01)
                    try:
                        while 1:
                            master.send_processdata()
                            master.receive_processdata(1_000)
                            time.sleep(0.01)
                    except KeyboardInterrupt:
                        print('stopped')
                    # zero everything
                    tmcm1617.output = bytes(len(tmcm1617.output))
                    master.send_processdata()
                    master.receive_processdata(1_000)
                else:
                    print('failed to got to op state')
            else:
                print('failed to got to safeop state')
            master.state = pysoem.PREOP_STATE
            master.write_state()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
