# This Python file uses the following encoding: utf-8
import sys
import PyQt5
import pysoem
import time
import ctypes
import struct

from PySide6.QtWidgets import QApplication, QWidget,QMessageBox
from PyQt5.QtGui import QGuiApplication

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

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
    'Profile Torque mode': 4,
    'Homing mode': 6,
    'Cyclic synchronous position mode': 8,
    'Cyclic synchronous velocity mode': 9,
    'Cyclic synchronous torque mode': 10,
}

# Define constants for control commands
CONTROLWORD_START = 0x000F  # Start/Enable
CONTROLWORD_STOP = 0x0000  # Stop/Disable

def convert_input_data(data):
    return InputPdo.from_buffer_copy(data)

def set_mode_of_operation(slave, mode):
    print("Setting the mode of operation: ...")
    if mode in modes_of_operation:
        mode_value = modes_of_operation[mode]
        try:
            slave.sdo_write(0x6060, 0, mode_value, pysoem.INT8)
            #slave.sdo_write(0x6060, 0, mode_value.to_bytes(length=1, byteorder='little', signed=True))
            #slave.sdo_write(index=0x6060, subindex=0, data=struct.pack("B", mode_value))
            print(f"Mode of Operation set to: {mode} ({mode_value})")
        except Exception as e:
            print(e)
    else:
        print(f"Invalid mode of operation: {mode}")

def set_target_speed(slave, target_speed):
    print("Setting the target speed: ...")
    try:
        TARGET_VELOCITY_INDEX = 0x60FF  # Target Velocity (assuming this is the index for velocity)
        slave.sdo_write(TARGET_VELOCITY_INDEX, 0, target_speed, pysoem.INT32)
        #slave.sdo_write(TARGET_VELOCITY_INDEX, 0, target_speed)
        #slave.sdo_write(index=0x60FF, subindex=0, data=struct.pack("B", target_speed))
        print(f"Set Target Speed to: {target_speed} RPM")
    except Exception as e:
        print(e)

def set_target_torque(slave, target_torque):
    print("Setting the target torque: ...")
    try:
        TARGET_TORQUE_INDEX = 0x6071
        slave.sdo_write(TARGET_TORQUE_INDEX, 0, target_torque, pysoem.INT16)
        #slave.sdo_write(TARGET_TORQUE_INDEX, 0, target_torque)
        #slave.sdo_write(index=0x6071, subindex=0, data=struct.pack("B", target_torque))
        print(f"Set Target Torque to: {target_torque} Nm")
    except Exception as e:
        print(e)


def control_motor(slave, controlword):
    print("Setting the target torque: ...")
    try:
        CONTROLWORD_INDEX = 0x6040  # Control Word index (adjust if needed)
        slave.sdo_write(CONTROLWORD_INDEX, 0, controlword, pysoem.INT16)
        #slave.sdo_write(index=0x6040, subindex=0, data=struct.pack("B", controlword))
        print(f"Motor control command sent: {controlword}")
    except Exception as e:
        print(e)


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        #self.center()  # Call the center method

        # Initialize the master object
        self.master = None  # Initially, the master is not connected
        self.master_opened = False  # Boolean flag to track if master is opened

        self.ui.FindAdapter.clicked.connect(self.FindAdFunc)
        self.ui.pushButton_open.clicked.connect(self.OpenEthercat)
        self.ui.pushButton_Close.clicked.connect(self.CloseEthercat)
        self.ui.pushButton_move.clicked.connect(self.move_servo)
        self.ui.pushButton_Stop.clicked.connect(self.stop_servo)
        self.ui.CloseB.clicked.connect(self.Close)
        self.ui.pushButton_move_2.clicked.connect(self.move_servo_2)
        self.ui.pushButton_Stop_2.clicked.connect(self.stop_servo_2)


        self.ui.ModeOfOperation.addItem("No mode", 0)
        self.ui.ModeOfOperation.addItem("Profile position mode", 1)
        self.ui.ModeOfOperation.addItem("Profile velocity mode", 3)
        self.ui.ModeOfOperation.addItem("Profile Torque mode", 4)
        self.ui.ModeOfOperation.addItem("Homing mode", 6)
        self.ui.ModeOfOperation.addItem("Cyclic synchronous position mode", 8)
        self.ui.ModeOfOperation.addItem("Cyclic synchronous velocity mode", 9)
        self.ui.ModeOfOperation.addItem("Cyclic synchronous torque mode", 10)


        self.ui.ApplySetB.clicked.connect(self.ApplySet)

    def Close(self):
        self.close();

    def ApplySet(self):

        self.master.state = pysoem.PREOP_STATE
        self.master.write_state()
        self.master.read_state()
        if self.master.state != pysoem.PREOP_STATE:
            print("Failed to enter PRE-OP state.")
        else:
            print("PRE-OP state successfilly changed")

        selected_mode = self.ui.ModeOfOperation.currentText()
        #target_speed = (self.ui.spinBox_TargetVelocity.value()).to_bytes(length=4, byteorder='little', signed=False)
        #target_torque = (self.ui.spinBox_TargetTorque.value()).to_bytes(length=2, byteorder='little', signed=False)

        target_speed = self.ui.spinBox_TargetVelocity.value()
        target_torque = self.ui.spinBox_TargetTorque.value()

        print(f"Selected mode: {selected_mode}, Target Speed: {target_speed}, Target Torque: {target_torque}")

        try:

            selected_slave_index = self.ui.Combo_Slaves.currentIndex()


            if selected_slave_index == -1:
                print("Please select a servo motor")
                return

            print(f"selected {selected_slave_index+1} servo motor")
            servo_slave = self.master.slaves[selected_slave_index]

            set_mode_of_operation(servo_slave, selected_mode)

            # Set target speed and torque
            set_target_speed(servo_slave, target_speed)
            set_target_torque(servo_slave, target_torque)

        except Exception as e:
            print(e)

    def move_servo(self):
        """Configure the selected servo motor using SDOs and PDOs"""
        selected_slave_index = self.ui.Combo_Slaves.currentIndex()


        if selected_slave_index == -1:
            print("Please select a servo motor")
            return

        servo_slave = self.master.slaves[selected_slave_index]

        try:
            control_motor(servo_slave, CONTROLWORD_START)
            print("Motor is now moving.")
        except:
            print("No slaves found.")

    def stop_servo(self):

        """Configure the selected servo motor using SDOs and PDOs"""
        selected_slave_index = self.ui.Combo_Slaves.currentIndex()


        if selected_slave_index == -1:
            print("Please select a servo motor")
            return

        servo_slave = self.master.slaves[selected_slave_index]

        try:
            control_motor(servo_slave, CONTROLWORD_STOP)
            print("Motor has been stopped.")
        except:
            print("Error: No slaves found.")

    def CloseEthercat(self):

        if self.master and self.master_opened:
            self.master.close()
            self.master_opened = False  # Set the flag to False when closed
            self.master = None
            print("EtherCAT master closed")
        else:
            print("Master is not opened")

    def OpenEthercat(self):
        if self.master is None:

            etherCat = self.ui.Combo_Adapter.currentText()
            self.ui.Combo_Slaves.clear()
            self.master = pysoem.Master()
            self.master_opened = True
            try:
                self.master.open(etherCat)
                if self.master.config_init() > 0:
                    print('Master is opened')
                    self.open_flag = 1
                    #self.master.detect_slaves()  # Detect slaves on the network
                    # Populate the slave combo box
                    for i, slave in enumerate(self.master.slaves):
                        slave_name = getattr(slave, 'name', f"Unknown Slave {i+1}")
                        self.ui.Combo_Slaves.addItem(f"Slave {i+1}: {slave_name}", slave)
                else:
                    print('no device found')
            except Exception as e:
                print(e)
        else:
            print('Invalid Master Adress')

    def show_message(self,Text):
        msg = QMessageBox()
        #msg.setIcon(QMessageBox.Information)
        msg.setText(Text)
        msg.setWindowTitle("Message")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()  # Show the message box

    def FindAdFunc(self):
        self.ui.Combo_Adapter.clear()
        adapters = pysoem.find_adapters()
        if not adapters:
            print("No adapters found!")

        print("Available adapters founded")
        for i, adapter in enumerate(adapters):
            # Add adapter name and description as a combo box item
            self.ui.Combo_Adapter.addItem(f"{adapter.name}")

    def center(self):
        # Get the screen's geometry using QScreen instead of QDesktopWidget
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            print("Error: No screen detected.")
            return

        screen_geometry = screen.availableGeometry()

        # Get the center of the screen
        screen_center = screen_geometry.center()

        # Move the window to the center
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def move_servo_2(self):
       """Configure the selected servo motor using SDOs and PDOs"""
       slave_index = self.ui.Combo_Slaves.currentIndex()


       if slave_index == -1:
           print("Please select a servo motor")
           return

       target_velocity = self.ui.spinBox_TargetVelocity.value()
       try:
           # Step 1: Transition the EtherCAT network to Pre-Operational state
           self.master.state = pysoem.PREOP_STATE
           self.master.write_state()
           self.master.read_state()
           if self.master.state != pysoem.PREOP_STATE:
               print("Failed to enter PRE-OP state.")
           else:
                print("PRE-OP state changed.")

           # Step 2: Get the specific servo motor (slave)
           servo_motor = self.master.slaves[slave_index]

           # Step 3: Set the operating mode to Speed Profile Mode
           # Speed Profile Mode is typically set via SDO 0x6060 with the value of 0x03
           print("step 3: ...")
           servo_motor.sdo_write(index=0x6060, subindex=0, data=struct.pack("B", 3))

           # Step 4: Set the Control Word to switch on the servo motor
           # Control Word 0x6040: 0x06 (enable voltage), 0x07 (enable operation)
           print("step 4: ...")
           servo_motor.sdo_write(index=0x6040, subindex=0, data=0x06)
           servo_motor.sdo_write(index=0x6040, subindex=0, data=0x07)

           # Step 5: Set the target velocity via SDO 0x60FF
           # Example: Write the target velocity to the servo motor
           print("step 5: ...")
           servo_motor.sdo_write(index=0x60FF, subindex=0, data=struct.pack("B", target_velocity))

           # Step 6: Transition the EtherCAT network to Operational state
           self.master.state = pysoem.OP_STATE
           self.master.write_state()
           self.master.read_state()

           if self.master.state != pysoem.OP_STATE:
               print("Failed to enter OP state.")

           print(f"Servo motor {servo_motor.name} is configured for Speed Profile Mode with velocity {target_velocity}.")
           #self.status_label.setText(f"Servo {servo_motor.name} in Speed Profile Mode.")

       except Exception as e:
           print(f"Error configuring servo motor in Speed Profile Mode: {e}")
           print(f"Error: {e}")

    def stop_servo_2(self):

       """
       Stops the HCFA Y7 servo motor by sending the stop command.

       :param slave_index: Index of the slave (servo motor) to stop.
       """
       selected_slave_index = self.ui.Combo_Slaves.currentIndex()


       if selected_slave_index == -1:
           print("Please select a servo motor")
           return

       try:
           # Step 1: Get the specific servo motor (slave)
           servo_motor = self.master.slaves[selected_slave_index]

           # Step 2: Set the target velocity to 0 to stop the motor
           # SDO 0x60FF is used to set the target velocity.
           print("step 2: ...")
           servo_motor.sdo_write(index=0x60FF, subindex=0, data=struct.pack("B", 0))

           # Step 3: Set the Control Word to stop the motor
           # Control Word 0x6040: Set it to 0x06 to disable operation
           print("step 3: ...")
           servo_motor.sdo_write(index=0x60FF, subindex=0, data=0x06)


           print(f"Servo motor {servo_motor.name} is stopped.")
           print(f"Servo {servo_motor.name} stopped.")

       except Exception as e:
           print(f"Error stopping the servo motor: {e}")
           print(f"Error: {e}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.setWindowTitle("Controlling Servo Motors")
    #widget.resize(500, 200)
    widget.show()
    sys.exit(app.exec())
