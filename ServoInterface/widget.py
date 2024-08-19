# This Python file uses the following encoding: utf-8
import sys
import PyQt5
import pysoem

from PySide6.QtWidgets import QApplication, QWidget,QMessageBox
from PyQt5.QtGui import QGuiApplication

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.center()  # Call the center method

        # Initialize the master object
        self.master = None  # Initially, the master is not connected
        self.master_opened = False  # Boolean flag to track if master is opened

        self.ui.FindAdapter.clicked.connect(self.FindAdFunc)
        self.ui.pushButton_open.clicked.connect(self.OpenEthercat)
        self.ui.pushButton_Close.clicked.connect(self.CloseEthercat)
        self.ui.pushButton_move.clicked.connect(self.move_servo)
        self.ui.pushButton_Stop.clicked.connect(self.stop_servo)

    def move_servo(self):
        """Configure the selected servo motor using SDOs and PDOs"""
        selected_slave_index = self.ui.Combo_Slaves.currentIndex()


        if selected_slave_index == -1:
            self.show_message("Please select a servo motor")
            return

        target_velocity = self.ui.spinBox_TargetVelocity.value()
        self.configure_speed_profile_mode(selected_slave_index, target_velocity)
    def stop_servo(self):

        """
        Stops the HCFA Y7 servo motor by sending the stop command.

        :param slave_index: Index of the slave (servo motor) to stop.
        """
        selected_slave_index = self.ui.Combo_Slaves.currentIndex()


        if selected_slave_index == -1:
            self.show_message("Please select a servo motor")
            return

        try:
            # Step 1: Get the specific servo motor (slave)
            servo_motor = self.master.slaves[selected_slave_index]

            # Step 2: Set the target velocity to 0 to stop the motor
            # SDO 0x60FF is used to set the target velocity.
            servo_motor.sdo_write(0x60FF, 0, 0)

            # Step 3: Set the Control Word to stop the motor
            # Control Word 0x6040: Set it to 0x06 to disable operation
            servo_motor.sdo_write(0x6040, 0, 0x06)  # Disable operation

            print(f"Servo motor {servo_motor.name} is stopped.")
            self.show_message(f"Servo {servo_motor.name} stopped.")

        except Exception as e:
            print(f"Error stopping the servo motor: {e}")
            self.show_message(f"Error: {e}")

    def CloseEthercat(self):

        if self.master and self.master_opened:
            self.master.close()
            self.master_opened = False  # Set the flag to False when closed
            self.master = None
            self.show_message("EtherCAT master closed")
        else:
            self.show_message("Master is not opened")

    def OpenEthercat(self):
        if self.master is None:

            etherCat = self.ui.Combo_Adapter.currentText()
            self.ui.Combo_Slaves.clear()
            self.master = pysoem.Master()
            self.master_opened = True
            try:
                self.master.open(etherCat)
                if self.master.config_init() > 0:
                    self.show_message('Master is opened')
                    self.open_flag = 1
                   # self.master.detect_slaves()  # Detect slaves on the network
                    # Populate the slave combo box
                    for i, slave in enumerate(self.master.slaves):
                        slave_info = f"Slave {i}: {slave.name} ({slave.type})"
                        self.Combo_Slaves.addItem(slave_info)
                else:
                    self.show_message('no device found')
            except:
                self.show_message('Invalid Master adress')
        else:
             self.show_message("Master already connected")

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
            self.show_message("No adapters found!")

        self.show_message("Available adapters founded")
        for i, adapter in enumerate(adapters):
            # Add adapter name and description as a combo box item
            self.ui.Combo_Adapter.addItem(f"{adapter.name}")

    def configure_speed_profile_mode(self, slave_index, target_velocity):
        """
        Configures the HCFA Y7 servo motor to operate in Speed Profile Mode.

        :param slave_index: Index of the slave (servo motor) to configure.
        :param target_velocity: The desired target velocity in the appropriate units.
        """
        try:
            # Step 1: Transition the EtherCAT network to Pre-Operational state
            self.master.state = pysoem.PREOP_STATE
            self.master.write_state()
            self.master.read_state()
            if self.master.state != pysoem.PREOP_STATE:
                self.show_message("Failed to enter PRE-OP state.")

            # Step 2: Get the specific servo motor (slave)
            servo_motor = self.master.slaves[slave_index]

            # Step 3: Set the operating mode to Speed Profile Mode
            # Speed Profile Mode is typically set via SDO 0x6060 with the value of 0x03
            servo_motor.sdo_write(0x6060, 0, 3)  # 0x03 corresponds to Speed Profile Mode

            # Step 4: Set the Control Word to switch on the servo motor
            # Control Word 0x6040: 0x06 (enable voltage), 0x07 (enable operation)
            servo_motor.sdo_write(0x6040, 0, 0x06)  # Enable voltage
            servo_motor.sdo_write(0x6040, 0, 0x07)  # Enable operation

            # Step 5: Set the target velocity via SDO 0x60FF
            # Example: Write the target velocity to the servo motor
            servo_motor.sdo_write(0x60FF, 0, target_velocity)

            # Step 6: Transition the EtherCAT network to Operational state
            self.master.state = pysoem.OP_STATE
            self.master.write_state()
            self.master.read_state()

            if self.master.state != pysoem.OP_STATE:
                self.show_message("Failed to enter OP state.")

            self.show_message(f"Servo motor {servo_motor.name} is configured for Speed Profile Mode with velocity {target_velocity}.")
            #self.status_label.setText(f"Servo {servo_motor.name} in Speed Profile Mode.")

        except Exception as e:
            print(f"Error configuring servo motor in Speed Profile Mode: {e}")
            self.show_message(f"Error: {e}")
    def stop_servo_motor(self, slave_index):
        """
        Stops the HCFA Y7 servo motor by sending the stop command.

        :param slave_index: Index of the slave (servo motor) to stop.
        """
        try:
            # Step 1: Get the specific servo motor (slave)
            servo_motor = self.master.slaves[slave_index]

            # Step 2: Set the target velocity to 0 to stop the motor
            # SDO 0x60FF is used to set the target velocity.
            servo_motor.sdo_write(0x60FF, 0, 0)

            # Step 3: Set the Control Word to stop the motor
            # Control Word 0x6040: Set it to 0x06 to disable operation
            servo_motor.sdo_write(0x6040, 0, 0x06)  # Disable operation

            self.show_message(f"Servo motor {servo_motor.name} is stopped.")

        except Exception as e:
            print(f"Error stopping the servo motor: {e}")
            self.status_label.setText(f"Error: {e}")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.setWindowTitle("Controlling Servo Motors")
    #widget.resize(500, 200)
    widget.show()
    sys.exit(app.exec())
