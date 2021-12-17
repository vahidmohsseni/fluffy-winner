from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import random
import requests
port = 5000
base_url = 'http://iot.vahid.click/'


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # define central widget
        self.main_widget = QtWidgets.QTabWidget()

        # define the start layout
        self.start_layout = QtWidgets.QVBoxLayout()

        # define welcome message
        self.start_layout_message = QtWidgets.QLabel('\n\nWelcome\nto\nSmart watering system\nsimulator!')
        self.start_layout_message.setStyleSheet('color: purple')
        self.start_layout_message.setFont(QtGui.QFont('Arial', 30))
        self.start_layout_message.setAlignment(QtCore.Qt.AlignCenter)

        # define start button
        self.start_working_btn = QtWidgets.QPushButton('Start')
        self.start_working_btn.setFixedSize(100, 100)

        # define toolbar
        self.toolbar = QtWidgets.QToolBar('Main toolbar')

        # define refresh action in toolbar
        self.refresh_action = QtWidgets.QAction(QtGui.QIcon('icons/refresh.png'), '&refresh', self)
        self.refresh_action.triggered.connect(self.refresh_app)

        # add refresh to toolbar
        self.toolbar.addAction(self.refresh_action)

        # define main layout for locations
        self.main_layout = QtWidgets.QHBoxLayout()

        # sends data to servery
        self.main_timer = QtCore.QTimer()
        self.main_timer_period = 1000 * 10

        # change the value of sensors
        self.change_sensors_timer = QtCore.QTimer()
        self.change_sensors_timer_period = 1000 * 5

        # enable actuators for a certion period
        self.change_actuator_timer = QtCore.QTimer()
        self.change_actuator_timer_period = 1000 * 3

        # change the temperature of locations
        self.change_temp_timer = QtCore.QTimer()
        self.change_temp_timer_period = 1000 * 15

        self.lock_sensors = False
        self.lock_temp = False
        self.refresh_lock = False

        self.actuator_use_timer = False

        # initializing locations
        resp = requests.get(base_url + "/init_sim")
        response = resp.json()

        self.num_locations = response['num_locations']
        self.locations = []
        for i in range(self.num_locations):
            self.locations.append({'location_id': response['locations_data'][i]['location_id'],
                                   'name': response['locations_data'][i]['location_name'],
                                   'num_instances': response['locations_data'][i]['num_instances'],
                                   'layout': QtWidgets.QVBoxLayout(),
                                   'temp': QtWidgets.QHBoxLayout(),
                                   'temp_label': QtWidgets.QLabel('Room temperature'),
                                   'name_label': QtWidgets.QLabel(),
                                   'instances': [],
                                   'instances_ids': response['locations_data'][i]['instances_ids'],
                                   'pics': [],
                                   'list_of_pics': response['locations_data'][i]['list_of_pics'],
                                   'pixmaps': [],
                                   'inventory': [],
                                   'moist_sensors': [],
                                   'moist_sensors_labels': [],
                                   'moist_sensors_values': [],
                                   'ph_sensors': [],
                                   'ph_sensors_labels': [],
                                   'ph_sensors_values': [],
                                   'actuators': [],
                                   'actuators_labels': [],
                                   'actuators_values': [],
                                   'list_of_changed_sensors': [],
                                   'watere_needed_instances': [],
                                   'list_of_changed_instances': [],
                                   })

        # This is for the sake of UI representing and window size
        self.max_instances = 0
        for i in range(self.num_locations):
            if self.max_instances < self.locations[i]['num_instances']:
                self.max_instances = self.locations[i]['num_instances']

        # mark instances that are needed to be watered so that their correspondence sensors' values change properly
        for i in range(self.num_locations):
            for j in range(self.locations[i]['num_instances']):
                self.locations[i]['watere_needed_instances'].append(False)

        # initializing the widgets and layouts of each location
        for i in range(self.num_locations):
            self.locations[i]['temp_label'].setText('Room temperature')
            self.locations[i]['temp_label'].setFont(QtGui.QFont('Arial', 10))
            self.locations[i]['temp_label'].setAlignment(QtCore.Qt.AlignCenter)

            self.locations[i]['name_label'].setText(self.locations[i]['name'])
            self.locations[i]['name_label'].setFont(QtGui.QFont('Arial', 20))
            self.locations[i]['name_label'].setAlignment(QtCore.Qt.AlignCenter)

            for j in range(self.locations[i]['num_instances']):
                self.locations[i]['instances'].append(QtWidgets.QVBoxLayout())
                self.locations[i]['pics'].append(QtWidgets.QLabel())
                self.locations[i]['pixmaps'].append(QtGui.QPixmap(self.locations[i]['list_of_pics'][j]))

                self.locations[i]['inventory'].append(QtWidgets.QHBoxLayout())

                self.locations[i]['moist_sensors'].append(QtWidgets.QVBoxLayout())

                self.locations[i]['moist_sensors_labels'].append(QtWidgets.QLabel('Moisture'))
                self.locations[i]['moist_sensors_labels'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['moist_sensors_labels'][j].setStyleSheet("background-color: lightblue")
                self.locations[i]['moist_sensors_labels'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['moist_sensors_labels'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['moist_sensors_values'].append(QtWidgets.QLabel())
                self.locations[i]['moist_sensors_values'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['moist_sensors_values'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['moist_sensors_values'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['ph_sensors'].append(QtWidgets.QVBoxLayout())

                self.locations[i]['ph_sensors_labels'].append(QtWidgets.QLabel('PH'))
                self.locations[i]['ph_sensors_labels'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['ph_sensors_labels'][j].setStyleSheet("background-color: yellow")
                self.locations[i]['ph_sensors_labels'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['ph_sensors_labels'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['ph_sensors_values'].append(QtWidgets.QLabel())
                self.locations[i]['ph_sensors_values'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['ph_sensors_values'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['ph_sensors_values'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['actuators'].append(QtWidgets.QVBoxLayout())

                self.locations[i]['actuators_labels'].append(QtWidgets.QLabel('Actuator'))
                self.locations[i]['actuators_labels'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['actuators_labels'][j].setStyleSheet("background-color: grey")
                self.locations[i]['actuators_labels'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['actuators_labels'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['actuators_values'].append(QtWidgets.QLabel())
                self.locations[i]['actuators_values'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['actuators_values'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['actuators_values'][j].setAlignment(QtCore.Qt.AlignCenter)

        # for the sake of UI design, to be in a grid shape, we need to add some empty instances to fill the space
        self.list_of_fake_layouts = []
        self.list_of_fake_pics = []
        self.list_of_fake_sensors = []
        self.list_of_fake_sensors_labels = []
        self.list_of_fake_sensors_values = []
        for i in range(self.num_locations):
            self.list_of_fake_layouts.append([])
            self.list_of_fake_pics.append([])
            self.list_of_fake_sensors.append([])
            self.list_of_fake_sensors_labels.append([])
            self.list_of_fake_sensors_values.append([])
            for j in range(self.max_instances - self.locations[i]['num_instances']):
                self.list_of_fake_layouts[i].append(QtWidgets.QVBoxLayout())

                self.list_of_fake_pics[i].append(QtWidgets.QLabel())
                self.list_of_fake_pics[i][j].setFixedSize(250, 250)

                self.list_of_fake_layouts[i][j].addWidget(self.list_of_fake_pics[i][j])

                self.list_of_fake_sensors[i].append(QtWidgets.QVBoxLayout())

                self.list_of_fake_sensors_labels[i].append(QtWidgets.QLabel())
                self.list_of_fake_sensors_labels[i][j].setFont(QtGui.QFont('Arial', 10))
                self.list_of_fake_sensors_labels[i][j].setFixedSize(140, 40)

                self.list_of_fake_sensors[i][j].addWidget(self.list_of_fake_sensors_labels[i][j])

                self.list_of_fake_sensors_values[i].append(QtWidgets.QLabel())
                self.list_of_fake_sensors_values[i][j].setFont(QtGui.QFont('Arial', 10))
                self.list_of_fake_sensors_values[i][j].setFixedSize(140, 40)

                self.list_of_fake_sensors[i][j].addWidget(self.list_of_fake_sensors_values[i][j])

                self.list_of_fake_layouts[i][j].addLayout(self.list_of_fake_sensors[i][j])

        self.start_ui()
        self.init_ui()

    def start_ui(self):
        self.main_timer.start(self.main_timer_period)
        self.change_sensors_timer.start(self.change_sensors_timer_period)
        self.change_temp_timer.start(self.change_temp_timer_period)

    def init_ui(self):
        self.setWindowTitle('Smart irrigation system simulator')
        self.setGeometry(1200, 200, 900, 900)
        self.setCentralWidget(self.main_widget)

        self.start_layout.addWidget(self.start_layout_message)
        self.start_layout.addWidget(self.start_working_btn, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.start_layout)
        self.start_working_btn.clicked.connect(self.set_main_layout)

        self.main_widget.setLayout(self.main_layout)

    def set_main_layout(self):
        self.start_layout.removeWidget(self.start_layout_message)
        self.start_layout.removeWidget(self.start_working_btn)
        self.start_layout_message.deleteLater()
        self.start_working_btn.deleteLater()
        self.main_layout.removeItem(self.start_layout)
        self.start_layout.deleteLater()
        self.main_layout.removeWidget(self.start_layout_message)
        self.main_layout.removeWidget(self.start_working_btn)

        self.start_working()

    def start_working(self):
        # setting fixed size to all labels
        self.setting_size()

        self.setGeometry(1200, 200, self.num_locations * 480, 100 + self.max_instances * 390)

        for i in range(self.num_locations):
            self.init_location(i)

        for i in range(self.num_locations):
            self.main_layout.addLayout(self.locations[i]['layout'])

        self.addToolBar(self.toolbar)

        self.init_sensors()

        self.main_timer.timeout.connect(self.main_timer_triggered)
        self.change_sensors_timer.timeout.connect(self.change_sensors)
        self.change_temp_timer.timeout.connect(self.change_temp_sensors)

    def setting_size(self):
        for i in range(self.num_locations):
            self.locations[i]['name_label'].setFixedSize(480, 50)
            self.locations[i]['temp_label'].setFixedSize(480, 50)
            for j in range(self.locations[i]['num_instances']):
                # self.locations[i]['pics'][j].setFixedSize(250, 250)
                # self.locations[i]['pics'][j].setAlignment(QtCore.Qt.AlignCenter)
                self.locations[i]['moist_sensors_labels'][j].setFixedSize(140, 40)
                self.locations[i]['moist_sensors_values'][j].setFixedSize(140, 40)
                self.locations[i]['ph_sensors_labels'][j].setFixedSize(140, 40)
                self.locations[i]['ph_sensors_values'][j].setFixedSize(140, 40)
                self.locations[i]['actuators_labels'][j].setFixedSize(140, 40)
                self.locations[i]['actuators_values'][j].setFixedSize(140, 40)

    def init_sensors(self):
        # setting a random numbers between 18 and 22 per location
        for i in range(self.num_locations):
            self.locations[i]['temp_label'].setText('Room Temperature ' + str(random.randint(18, 22)))

        # setting random numbers per sensor (moisture between 30 and 60, ph between 0 and 14)
        for i in range(self.num_locations):
            for j in range(self.locations[i]['num_instances']):
                self.locations[i]['moist_sensors_values'][j].setText(str(random.randint(30, 60))+' %')
                self.locations[i]['ph_sensors_values'][j].setText(str(random.randint(4, 9)))

    def refresh_app(self):
        self.main_timer.stop()
        self.change_sensors_timer.stop()
        self.change_actuator_timer.stop()
        self.change_temp_timer.stop()

        self.refresh_lock = True
        resp = requests.get(base_url + "/init_sim")
        response = resp.json()

        self.delete_everything()
        self.rebuild_everything(response)

        self.refresh_lock = False
        self.init_sensors()
        self.main_timer.start()
        self.change_sensors_timer.start()
        self.change_temp_timer.start()

    def delete_everything(self):
        for i in range(self.num_locations):
            self.delete_pics(i)
            self.delete_inventory(i)
            self.delete_location(i)
            self.delete_fake(i)

    def delete_fake(self, location_id):
        for i in range(self.max_instances - self.locations[location_id]['num_instances']):
            self.list_of_fake_layouts[location_id][i].removeWidget(self.list_of_fake_pics[location_id][i])
            self.list_of_fake_pics[location_id][i].deleteLater()

            self.list_of_fake_sensors[location_id][i].removeWidget(self.list_of_fake_sensors_values[location_id][i])
            self.list_of_fake_sensors_values[location_id][i].deleteLater()

            self.list_of_fake_sensors[location_id][i].removeWidget(self.list_of_fake_sensors_labels[location_id][i])
            self.list_of_fake_sensors_labels[location_id][i].deleteLater()

            self.list_of_fake_layouts[location_id][i].removeItem(self.list_of_fake_sensors[location_id][i])

            self.locations[location_id]['layout'].removeItem(self.list_of_fake_layouts[location_id][i])
            self.list_of_fake_layouts[location_id][i].deleteLater()

    def delete_pics(self, location_id):
        for i in range(self.locations[location_id]['num_instances']):
            self.locations[location_id]['instances'][i].removeWidget(self.locations[location_id]['pics'][i])
            self.locations[location_id]['pics'][i].deleteLater()

    def delete_inventory(self, location_id):
        for i in range(self.locations[location_id]['num_instances']):
            self.locations[location_id]['moist_sensors'][i].removeWidget(self.locations[location_id]['moist_sensors_labels'][i])
            self.locations[location_id]['moist_sensors_labels'][i].deleteLater()

            self.locations[location_id]['moist_sensors'][i].removeWidget(self.locations[location_id]['moist_sensors_values'][i])
            self.locations[location_id]['moist_sensors_values'][i].deleteLater()

            self.locations[location_id]['inventory'][i].removeItem(self.locations[location_id]['moist_sensors'][i])

            self.locations[location_id]['ph_sensors'][i].removeWidget(self.locations[location_id]['ph_sensors_labels'][i])
            self.locations[location_id]['ph_sensors_labels'][i].deleteLater()

            self.locations[location_id]['ph_sensors'][i].removeWidget(self.locations[location_id]['ph_sensors_values'][i])
            self.locations[location_id]['ph_sensors_values'][i].deleteLater()

            self.locations[location_id]['inventory'][i].removeItem(self.locations[location_id]['ph_sensors'][i])

            self.locations[location_id]['actuators'][i].removeWidget(self.locations[location_id]['actuators_labels'][i])
            self.locations[location_id]['actuators_labels'][i].deleteLater()

            self.locations[location_id]['actuators'][i].removeWidget(self.locations[location_id]['actuators_values'][i])
            self.locations[location_id]['actuators_values'][i].deleteLater()

            self.locations[location_id]['inventory'][i].removeItem(self.locations[location_id]['actuators'][i])

            self.locations[location_id]['instances'][i].removeItem(self.locations[location_id]['inventory'][i])
            self.locations[location_id]['inventory'][i].deleteLater()

            self.locations[location_id]['layout'].removeItem(self.locations[location_id]['instances'][i])
            self.locations[location_id]['instances'][i].deleteLater()

    def delete_location(self, location_id):
        self.locations[location_id]['temp'].removeWidget(self.locations[location_id]['temp_label'])
        self.locations[location_id]['temp_label'].deleteLater()

        self.locations[location_id]['layout'].removeItem(self.locations[location_id]['temp'])
        self.locations[location_id]['temp'].deleteLater()

        self.locations[location_id]['layout'].removeWidget(self.locations[location_id]['name_label'])
        self.locations[location_id]['name_label'].deleteLater()

        self.main_layout.removeItem(self.locations[location_id]['layout'])
        self.main_layout.removeItem(self.locations[location_id]['layout'])
        self.locations[location_id]['layout'].deleteLater()

    def rebuild_everything(self, response):
        self.num_locations = response['num_locations']
        self.locations = []
        for i in range(self.num_locations):
            self.locations.append({'location_id': response['locations_data'][i]['location_id'],
                                   'name': response['locations_data'][i]['location_name'],
                                   'num_instances': response['locations_data'][i]['num_instances'],
                                   'layout': QtWidgets.QVBoxLayout(),
                                   'temp': QtWidgets.QHBoxLayout(),
                                   'temp_label': QtWidgets.QLabel('Room temperature'),
                                   'name_label': QtWidgets.QLabel(),
                                   'instances': [],
                                   'instances_ids': response['locations_data'][i]['instances_ids'],
                                   'pics': [],
                                   'list_of_pics': response['locations_data'][i]['list_of_pics'],
                                   'pixmaps': [],
                                   'inventory': [],
                                   'moist_sensors': [],
                                   'moist_sensors_labels': [],
                                   'moist_sensors_values': [],
                                   'ph_sensors': [],
                                   'ph_sensors_labels': [],
                                   'ph_sensors_values': [],
                                   'actuators': [],
                                   'actuators_labels': [],
                                   'actuators_values': [],
                                   'list_of_changed_sensors': [],
                                   'watere_needed_instances': [],
                                   'list_of_changed_instances': [],
                                   })

        self.max_instances = 0
        for i in range(self.num_locations):
            if self.max_instances < self.locations[i]['num_instances']:
                self.max_instances = self.locations[i]['num_instances']

        for i in range(self.num_locations):
            for j in range(self.locations[i]['num_instances']):
                self.locations[i]['watere_needed_instances'].append(False)

        for i in range(self.num_locations):
            self.locations[i]['temp_label'].setText('Room temperature')
            self.locations[i]['temp_label'].setFont(QtGui.QFont('Arial', 10))
            self.locations[i]['temp_label'].setAlignment(QtCore.Qt.AlignCenter)

            self.locations[i]['name_label'].setText(self.locations[i]['name'])
            self.locations[i]['name_label'].setFont(QtGui.QFont('Arial', 20))
            self.locations[i]['name_label'].setAlignment(QtCore.Qt.AlignCenter)

            for j in range(self.locations[i]['num_instances']):
                self.locations[i]['instances'].append(QtWidgets.QVBoxLayout())
                self.locations[i]['pics'].append(QtWidgets.QLabel())
                self.locations[i]['pixmaps'].append(QtGui.QPixmap(self.locations[i]['list_of_pics'][j]))

                self.locations[i]['inventory'].append(QtWidgets.QHBoxLayout())

                self.locations[i]['moist_sensors'].append(QtWidgets.QVBoxLayout())

                self.locations[i]['moist_sensors_labels'].append(QtWidgets.QLabel('Moisture'))
                self.locations[i]['moist_sensors_labels'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['moist_sensors_labels'][j].setStyleSheet("background-color: lightblue")
                self.locations[i]['moist_sensors_labels'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['moist_sensors_labels'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['moist_sensors_values'].append(QtWidgets.QLabel())
                self.locations[i]['moist_sensors_values'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['moist_sensors_values'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['moist_sensors_values'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['ph_sensors'].append(QtWidgets.QVBoxLayout())

                self.locations[i]['ph_sensors_labels'].append(QtWidgets.QLabel('PH'))
                self.locations[i]['ph_sensors_labels'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['ph_sensors_labels'][j].setStyleSheet("background-color: yellow")
                self.locations[i]['ph_sensors_labels'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['ph_sensors_labels'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['ph_sensors_values'].append(QtWidgets.QLabel())
                self.locations[i]['ph_sensors_values'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['ph_sensors_values'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['ph_sensors_values'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['actuators'].append(QtWidgets.QVBoxLayout())

                self.locations[i]['actuators_labels'].append(QtWidgets.QLabel('Actuator'))
                self.locations[i]['actuators_labels'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['actuators_labels'][j].setStyleSheet("background-color: grey")
                self.locations[i]['actuators_labels'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['actuators_labels'][j].setAlignment(QtCore.Qt.AlignCenter)

                self.locations[i]['actuators_values'].append(QtWidgets.QLabel())
                self.locations[i]['actuators_values'][j].setFont(QtGui.QFont('Arial', 10))
                self.locations[i]['actuators_values'][j].setFrameStyle(QtWidgets.QFrame.Panel)
                self.locations[i]['actuators_values'][j].setAlignment(QtCore.Qt.AlignCenter)

        self.rebuild_fakes()
        for i in range(self.num_locations):
            self.init_location(i)

        self.setting_size()
        self.setGeometry(1200, 200, self.num_locations * 480, 100 + self.max_instances * 390)
        for i in range(self.num_locations):
            self.main_layout.addLayout(self.locations[i]['layout'])

    def rebuild_fakes(self):
        self.list_of_fake_layouts = []
        self.list_of_fake_pics = []
        self.list_of_fake_sensors = []
        self.list_of_fake_sensors_labels = []
        self.list_of_fake_sensors_values = []
        for i in range(self.num_locations):
            self.list_of_fake_layouts.append([])
            self.list_of_fake_pics.append([])
            self.list_of_fake_sensors.append([])
            self.list_of_fake_sensors_labels.append([])
            self.list_of_fake_sensors_values.append([])
            for j in range(self.max_instances - self.locations[i]['num_instances']):
                self.list_of_fake_layouts[i].append(QtWidgets.QVBoxLayout())

                self.list_of_fake_pics[i].append(QtWidgets.QLabel())
                self.list_of_fake_pics[i][j].setFixedSize(250, 250)

                self.list_of_fake_layouts[i][j].addWidget(self.list_of_fake_pics[i][j])

                self.list_of_fake_sensors[i].append(QtWidgets.QVBoxLayout())

                self.list_of_fake_sensors_labels[i].append(QtWidgets.QLabel())
                self.list_of_fake_sensors_labels[i][j].setFont(QtGui.QFont('Arial', 10))
                self.list_of_fake_sensors_labels[i][j].setFixedSize(140, 40)

                self.list_of_fake_sensors[i][j].addWidget(self.list_of_fake_sensors_labels[i][j])

                self.list_of_fake_sensors_values[i].append(QtWidgets.QLabel())
                self.list_of_fake_sensors_values[i][j].setFont(QtGui.QFont('Arial', 10))
                self.list_of_fake_sensors_values[i][j].setFixedSize(140, 40)

                self.list_of_fake_sensors[i][j].addWidget(self.list_of_fake_sensors_values[i][j])

                self.list_of_fake_layouts[i][j].addLayout(self.list_of_fake_sensors[i][j])

    def main_timer_triggered(self):
        if not self.refresh_lock:
            # send sensors data to server
            responses = []
            for i in range(self.num_locations):
                response = []
                for j in range(self.locations[i]['num_instances']):
                    data = {'location_id': self.locations[i]['location_id'],
                            'plant_id': self.locations[i]['instances_ids'][j],
                            'moisture_level': int(self.locations[i]['moist_sensors_values'][j].text()[:-2]),
                            'ph_level': int(self.locations[i]['ph_sensors_values'][j].text()),
                            'temperature': int(self.locations[i]['temp_label'].text()[17:])}
                    resp = requests.post(base_url + "/sensor", data=data)
                    response.append(resp.json())
                responses.append(response)

            # print(responses)
            for i in range(self.num_locations):
                for j in range(self.locations[i]['num_instances']):
                    if responses[i][j]['status'] == 'ok':
                        if responses[i][j]['needs_water']:
                            self.locations[i]['list_of_changed_instances'].append(j)
                    else:
                        print('Server did not respond properly.')

            self.enable_actuators()

    def enable_actuators(self):
        if not self.refresh_lock:
            for i in range(self.num_locations):
                if len(self.locations[i]['list_of_changed_instances']) > 0:
                    self.actuator_use_timer = True
                    self.lock_sensors = True
                    break
            for i in range(self.num_locations):
                for j in self.locations[i]['list_of_changed_instances']:
                    self.locations[i]['actuators_values'][j].setText('Enabled')
                    self.locations[i]['actuators_values'][j].setStyleSheet("background-color: #fa98fa")
                    self.locations[i]['watere_needed_instances'][j] = True

            if self.actuator_use_timer:
                self.change_actuator_timer.start(self.change_actuator_timer_period)
                self.change_actuator_timer.timeout.connect(self.disable_actuators)
                self.lock_sensors = False
                # self.change_sensors()

    def disable_actuators(self):
        for i in range(self.num_locations):
            for j in self.locations[i]['list_of_changed_instances']:
                self.locations[i]['actuators_values'][j].setText('Disabled')
                self.locations[i]['actuators_values'][j].setStyleSheet("background-color: None")

        self.change_actuator_timer.stop()
        self.actuator_use_timer = False

    def change_temp_sensors(self):
        # change the temperature of each room. 30% chance for increasing, 30% for decreasing, and 30% chance of no change
        if not self.refresh_lock:
            if not self.lock_temp:
                for i in range(self.num_locations):
                    value = random.randint(0, 2)  # 0: do nothing, 1: increase temp, 2: decrease temp

                    if value == 1:
                        self.locations[i]['temp_label'].setText('Room temperature ' + str(int(self.locations[i]['temp_label'].text()[17:]) + 1))
                    elif value == 2:
                        self.locations[i]['temp_label'].setText('Room temperature ' + str(int(self.locations[i]['temp_label'].text()[17:]) - 1))

    def change_sensors(self):
        # if water needed: add 5 level water and decrease level of ph
        # otherwise, decrease moist value with 50% chance, and increase ph value with 30% chance
        if not self.refresh_lock:
            if not self.lock_sensors:
                for i in range(self.num_locations):
                    for j in range(self.locations[i]['num_instances']):
                        moist_value = int(self.locations[i]['moist_sensors_values'][j].text()[:-2])
                        ph_value = int(self.locations[i]['ph_sensors_values'][j].text())
                        if self.locations[i]['watere_needed_instances'][j]:
                            moist_value += 5
                            ph_value -= 1
                        else:
                            value = random.randint(0, 10)
                            if value % 2 == 0:
                                moist_value -= 1

                            value = random.randint(0, 3)
                            if value == 1:
                                ph_value += 1

                        if moist_value > 100:
                            moist_value = 100
                        if moist_value < 0:
                            moist_value = 0

                        if ph_value < 0:
                            ph_value = 0
                        if ph_value > 14:
                            ph_value = 14
                        self.locations[i]['watere_needed_instances'][j] = False
                        self.locations[i]['moist_sensors_values'][j].setText(str(moist_value) + ' %')
                        self.locations[i]['ph_sensors_values'][j].setText(str(ph_value))

    def init_location(self, location_id):
        self.locations[location_id]['temp'].addWidget(self.locations[location_id]['temp_label'])
        self.locations[location_id]['layout'].addWidget(self.locations[location_id]['name_label'])
        self.locations[location_id]['layout'].addLayout(self.locations[location_id]['temp'])

        self.init_pics(location_id)
        self.init_inventory(location_id)
        self.init_fakes(location_id)

    def init_pics(self, location_id):
        for i in range(self.locations[location_id]['num_instances']):
            self.locations[location_id]['pics'][i].setPixmap(self.locations[location_id]['pixmaps'][i].scaled(250, 250, QtCore.Qt.KeepAspectRatio))

            self.locations[location_id]['pics'][i].setAlignment(QtCore.Qt.AlignCenter)
            self.locations[location_id]['instances'][i].addWidget(self.locations[location_id]['pics'][i])
            self.locations[location_id]['layout'].addLayout(self.locations[location_id]['instances'][i])

    def init_inventory(self, location_id):
        for i in range(self.locations[location_id]['num_instances']):
            self.locations[location_id]['moist_sensors'][i].addWidget(self.locations[location_id]['moist_sensors_labels'][i])
            self.locations[location_id]['moist_sensors'][i].addWidget(self.locations[location_id]['moist_sensors_values'][i])

            self.locations[location_id]['ph_sensors'][i].addWidget(self.locations[location_id]['ph_sensors_labels'][i])
            self.locations[location_id]['ph_sensors'][i].addWidget(self.locations[location_id]['ph_sensors_values'][i])

            self.locations[location_id]['actuators_values'][i].setText('Disabled')

            self.locations[location_id]['actuators'][i].addWidget(self.locations[location_id]['actuators_labels'][i])
            self.locations[location_id]['actuators'][i].addWidget(self.locations[location_id]['actuators_values'][i])

            self.locations[location_id]['inventory'][i].addLayout(self.locations[location_id]['moist_sensors'][i])
            self.locations[location_id]['inventory'][i].addLayout(self.locations[location_id]['ph_sensors'][i])
            self.locations[location_id]['inventory'][i].addLayout(self.locations[location_id]['actuators'][i])

            self.locations[location_id]['instances'][i].addLayout(self.locations[location_id]['inventory'][i])

    def init_fakes(self, location_id):
        for i in range(self.max_instances - self.locations[location_id]['num_instances']):
            self.locations[location_id]['layout'].addLayout(self.list_of_fake_layouts[location_id][i])


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
