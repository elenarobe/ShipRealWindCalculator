# ShipRealWindCalculator
Python GUI for processing, viewing and transmitting data obtained from a naval weather station 

Our application was designed with the help of Python and Qt Designer, and it proved to be more challenging than we initially anticipated. For this particular app, we used a Vaisala weather station, just like the ones on the ship. The goal was to create a graphical user interface for solving the problem of calculating the components of real wind (real wind direction and real wind speed) from the composition of ship wind and apparent wind. Although at first glance it may seem like a simple problem, putting it into practice involves several challenges given that the application is at the intersection of the sailing navigation and mathematical domains. 

In order to connect the purchased equipment, we had to take into account the fact that they are not simple equipment, but rather data transmission equipment. The instruments (GPS, direction sensor, depth sounder, AIS...) have a special connection and operation mode and are usually connected to the computer using a serial connection. In our case, the data that is transferred on that serial connection must be in NMEA0183 format for the instrument(s) and the computer to understand each other. Therefore, in order to connect the weather station in series to the computer, an additional serial-to-USB adapter (NMEA 0138 to USB adapter) had to be purchased. It should be noted that before connecting the USB adapter, a special software (called a "driver") provided by the hardware manufacturer had to be installed. When we connect the USB serial adapter to the computer, the driver will create a "virtual COM port." This means that for any software installed on the computer, the adapter will be seen and detected as a regular COM port (just like if the computer had a serial COM port).

![image](https://github.com/elenarobe/ShipRealWindCalculator/assets/121317737/c1809532-155b-43f2-b8f0-ceab80d4a69e)
Fig. 1 Representation of a functional diagram of the data acquisition-processing-interpretation circuit

The program design was developed entirely in Qt Designer. Qt Designer is a free (open source) software that allows building graphical user interfaces (GUIs) that can be programmed later with different programming languages. The software operates based on the "what-you-see-is-what-you-get" and "drag and drop" methods. Specifically, Qt offers a variety of widgets that can be customized individually to meet the user's requirements.

The algorithm implementation and programming of the new graphical interface (Fig. 4.2) was done with the Python programming language. Python is a dynamic, multi-paradigm, object-oriented programming language that emphasizes code cleanliness and simplicity. Its syntax allows developers to express some programming ideas in a clearer and more concise way than in other programming languages, such as C++. The development environment chosen for Python in our case was the Visual Studio Code software, which is also a free program.

![image](https://github.com/elenarobe/ShipRealWindCalculator/assets/121317737/91e1ef4c-5d97-4ec1-b7fd-7e790d133134)<br/>
Fig. 2 Main Window

Due to the change in the programming approach caused by the way the data flow is obtained, the strategy for interpreting the results has also been changed. Thus, since both input and output data are read and calculated in real-time continuously, the user has the option to plot the wind estimate graphically at any time they wish (Fig. 3). The resulting sequence can be immediately visualized and stored under the graph (Fig. 4).

![image](https://github.com/elenarobe/ShipRealWindCalculator/assets/121317737/4976a1e3-83c7-4db1-b266-3898a8fb5d11)
Fig. 3 Query calculation and plotting of data set.

![image](https://github.com/elenarobe/ShipRealWindCalculator/assets/121317737/f29e4e2c-e189-47f6-9b74-d3b98a3b3eb9)
Fig. 4 Query calculation and plotting of data set

